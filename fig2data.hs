import Biolab.Interfaces.MySql
import Biolab.Analysis.GrowthRate
import Biolab.Analysis.Utils
import Biolab.Analysis.Normalization
import Biolab.Types
import Biolab.Analysis.Types
import qualified Data.Vector as V
import Data.Time (UTCTime, NominalDiffTime)
import Text.CSV
import qualified Data.Vector.Unboxed as U
import qualified Data.Vector as V
import Data.Vector ((!))
import Statistics.Sample (Sample, mean)
import Statistics.LinearRegression (linearRegression, nonRandomRobustFit, defaultEstimationParameters, EstimationParameters(..))
import Data.Maybe (fromMaybe, isJust, fromJust)
import Data.Time (UTCTime, NominalDiffTime, diffUTCTime)
import Statistics.Function (sortBy)
import Data.Function (on)
import Control.Arrow ((***))
import Biolab.Analysis.Types
import Biolab.Types
import Biolab.Analysis.Utils
import System.Environment (getArgs)

listPairToList a b c = concatMap pairToList [a,b,c]

pairToList (a,b) = [a,b]

mes_well = Well 'e' 8

main = do
    args <- getArgs
    let file_name_prefix = args !! 0
    mes_abs <- get_abs mes_well
    mes_fl1 <- get_fls mes_well
    mes_fl2 <- get_fls2 mes_well

---------------
    let abs_times = getTimesFromUtc . asMes $ mes_abs
    let abs_vals = map (show . mVal) . V.toList . V.map snd $ asMes mes_abs
    let fl1_times = getTimesFromUtc . flMes $ mes_fl1
    let fl1_vals = map (show . mVal) . V.toList . V.map snd $ flMes mes_fl1
    let fl2_times = getTimesFromUtc . flMes $ mes_fl2
    let fl2_vals = map (show . mVal) . V.toList . V.map snd $ flMes mes_fl2
    writeFile (file_name_prefix ++ "1.csv") $ printCSV [abs_times,abs_vals,fl1_times,fl1_vals,fl2_times,fl2_vals]

    
    absgr <- get_gr_data get_abs
    fl1gr <- get_gr_data get_fls
    fl2gr <- get_gr_data get_fls2
    writeFile (file_name_prefix ++ "2.csv") $ printCSV $ listPairToList absgr fl1gr fl2gr

    (pas,pes) <- get_pae_data get_fls
    (pas2,pes2) <- get_pae_data get_fls2
    writeFile (file_name_prefix ++ "3.csv") $ printCSV $ [fst pas,snd pas,fst pas2,snd pas2]
    writeFile (file_name_prefix ++ "4.csv") $ printCSV $ [fst pes,snd pes,fst pes2,snd pes2]
-- 4 panels - the raw mesurements+fluorescence.
--          - growth rate of the two (using a relevant time window).
--          - promoter activity.
--          - protein abundance.
---------------------------------------
    return ()

window_size = 10

get_gr_data :: ColonySample a => (Well -> IO (a RawMeasurement)) -> IO (([String],[String]))
get_gr_data get_mes = do
    mes <- get_mes mes_well
    let normalized = normalizeFromInit mes
    let dts = V.map (\(x,Just y) -> (x,y)) . V.filter (not . (== Nothing) . snd) . modGrowthRate linearRegression window_size $ normalized
    let simp = (getTimes dts,map (show . (*3600)) . V.toList . V.map snd $ dts)
    return simp

get_pae_data :: ColonySample a => (Well -> IO (a RawMeasurement)) -> IO (([String],[String]),([String],[String]))
get_pae_data get_mes = do
    abs_mes <- get_abs mes_well
    fl_mes <- get_mes mes_well

    let normalized_abs = trim . snd . absoluteToRelativeTime . measurements . normalizeFromInit $ abs_mes

    let start_time = fst . V.head $ normalized_abs
    let time_interval = fst (normalized_abs ! (window_size - 1)) - fst (normalized_abs ! 0)
    let normalized_fl = V.dropWhile (\x -> 100 <= start_time - (fst x)) . trim . snd . absoluteToRelativeTime . measurements . normalizeFromInit $ fl_mes

    let abs_fit = modExpApprox linearRegression window_size $ normalized_abs
    let fl_fit = modExpApprox linearRegression window_size $ normalized_fl
    let pas = V.map (\(x,Just y) -> (x,y)) . V.filter (not . (== Nothing) . snd) $ V.zipWith (\x y -> (fst x, pa (snd x) (snd y) (fst x) time_interval)) abs_fit fl_fit
    let pes = V.map (\(x,Just y) -> (x,y)) . V.filter (not . (== Nothing) . snd) $ V.zipWith (\x y -> (fst x, pe (snd x) (snd y) (fst x) time_interval)) abs_fit fl_fit

    return ((getTimes pas,map show . V.toList . V.map snd $ pas),(getTimes pes,map show . V.toList . V.map snd $ pes))

linspace :: (Fractional a, Enum a) => Int -> (a,a) -> [a]
linspace len (start,end) = take len $ [start,start+interval..end]
    where
        interval = end - start / realToFrac len

pa :: Maybe (Double,Double) -> Maybe (Double,Double) -> NominalDiffTime -> NominalDiffTime -> Maybe Double
pa Nothing _ _ _ = Nothing
pa _ Nothing _ _ = Nothing
pa (Just (abs_a,abs_b)) (Just (fl_a,fl_b)) start length = Just $ (fl (start + length) - fl (start))/(sum . map abs . linspace 10 $ (start,start+length))
    where
        abs t = 2 ** (abs_a + (realToFrac t)*abs_b)
        fl t = 2 ** (fl_a + (realToFrac t)*fl_b)

pe :: Maybe (Double,Double) -> Maybe (Double,Double) -> NominalDiffTime -> NominalDiffTime -> Maybe Double
pe Nothing _ _ _ = Nothing
pe _ Nothing _ _ = Nothing
pe (Just (abs_a,abs_b)) (Just (fl_a,fl_b)) start length = Just $ (fl start)/(abs start)
    where
        abs t = 2 ** (abs_a + (realToFrac t)*abs_b)
        fl t = 2 ** (fl_a + (realToFrac t)*fl_b)

estimationParameters = defaultEstimationParameters {outlierFraction = 0.25}

sqb w = SampleQuery ["2013-02-12 13:46:13"] [0] [w] -- Coli good exp
-- sqb w = SampleQuery ["2013-02-07 16:42:52"] [0] [w] -- Coli bad exp
-- sqb w = SampleQuery ["2013-01-06 12:00:00"] [1] [w] -- Leeat exp

get_abs :: Well -> IO (AbsorbanceSample RawMeasurement)
get_abs w = do
    db_conf <- dbConnectInfo "db.conf"
    mes <- loadMes db_conf (sqb w)
    return $ (\(AbsorbanceMeasurement x) -> x) . head . filter filterAbs . snd . head $ mes

get_fls :: Well -> IO (FluorescenseSample RawMeasurement)
get_fls w = do
    db_conf <- dbConnectInfo "db.conf"
    mes <- loadMes db_conf (sqb w)
    return $ (\(FluorescenseMeasurement x) -> x) . head . filter (not . filterAbs) . snd . head $ mes

get_fls2 :: Well -> IO (FluorescenseSample RawMeasurement)
get_fls2 w = do
    db_conf <- dbConnectInfo "db.conf"
    mes <- loadMes db_conf (sqb w)
    return $ (\(FluorescenseMeasurement x) -> x) . head . tail . filter (not . filterAbs) . snd . head $ mes

getTimesFromUtc :: V.Vector (UTCTime,a) -> [String]
getTimesFromUtc = getTimes . snd . absoluteToRelativeTime

getTimes :: V.Vector (NominalDiffTime,a) -> [String]
getTimes ca = map ( show . (/3600) . realToFrac ) . V.toList . V.map fst $ ca

filterAbs (AbsorbanceMeasurement _) = True
filterAbs _ = False

modExpApprox :: (U.Vector Double -> U.Vector Double -> (Double,Double)) -> Int -> V.Vector (NominalDiffTime,NormalizedMeasurement) -> V.Vector (NominalDiffTime,Maybe (Double,Double))
modExpApprox fit window_size mes = V.fromList . map (modExpApproxWindow fit . V.take window_size) . takeWhile (\x -> V.length x >= window_size) . iterate V.tail . V.map (realToFrac *** (logBase 2 . nmVal)) $ mes

modExpApproxWindow :: (U.Vector Double -> U.Vector Double -> (Double,Double)) -> V.Vector (Double,Double) -> (NominalDiffTime,Maybe (Double,Double))
modExpApproxWindow fit v = (realToFrac . fst $ v ! 0, modCalcExpFit fit v)

modCalcExpFit :: (U.Vector Double -> U.Vector Double -> (Double,Double)) -> V.Vector (Double,Double) -> Maybe (Double,Double)
modCalcExpFit fit xys = gr . fit xs $ ys
    where
        (xs,ys) = U.unzip . U.fromList . V.toList $ xys
        gr (x,y) = if y <=0 then Nothing else Just (x,y)

modGrowthRate :: (ColonySample a) => (U.Vector Double -> U.Vector Double -> (Double,Double)) -> Int -> a NormalizedMeasurement -> V.Vector (NominalDiffTime,Maybe Double)
modGrowthRate fit window_size mes = V.fromList . map (modGrowthRateWindow fit . V.take window_size) . takeWhile (\x -> V.length x >= window_size) . iterate V.tail . V.map (realToFrac *** (logBase 2 . nmVal)) . trim $ dmes
    where
        (start,dmes) = absoluteToRelativeTime . measurements $ mes

modGrowthRateWindow :: (U.Vector Double -> U.Vector Double -> (Double,Double)) -> V.Vector (Double,Double) -> (NominalDiffTime,Maybe Double)
modGrowthRateWindow fit v = (realToFrac . fst $ v ! 0 {-(window_size `div` 2) -},modCalcGrowthRate fit v)

modCalcGrowthRate :: (U.Vector Double -> U.Vector Double -> (Double,Double)) -> V.Vector (Double,Double) -> Maybe Double
modCalcGrowthRate fit xys = gr . snd . fit xs $ ys
    where
        (xs,ys) = U.unzip . U.fromList . V.toList $ xys
        gr x = if x <=0 then Nothing else Just x

