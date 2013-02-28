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
import Data.Maybe (fromMaybe, isJust, fromJust, catMaybes)
import Data.Time (UTCTime, NominalDiffTime, diffUTCTime)
import Statistics.Function (sortBy, sort)
import Data.Function (on)
import Control.Arrow ((***),(&&&))
import Biolab.Analysis.Types
import Biolab.Types
import Biolab.Analysis.Utils
import System.Environment (getArgs)
import Debug.Trace (trace)
import Data.List (elemIndices)

pairToList (a,b) = [a,b]

backgroundFromInitMod :: (ColonySample a) => (Double,Double) -> a RawMeasurement -> Maybe Background
backgroundFromInitMod (lower_bound,upper_bound) cs = if calc_mean > upper_bound || calc_mean < lower_bound then Nothing else Just . Background $ calc_mean
    where
        calc_mean = mean . V.init . V.tail . sort . V.map mVal . snd . V.unzip . V.take 5 . measurements $ cs

commonBegining :: (V.Vector (NominalDiffTime,Double),V.Vector (NominalDiffTime,Double)) -> (V.Vector (NominalDiffTime,Double),V.Vector (NominalDiffTime,Double))
commonBegining (abs,fl) = (t_abs,t_fl)
    where
        start_time = max (fst . V.head $ abs) (fst . V.head $ fl)
        t_abs = V.take window_size . V.dropWhile ((< start_time) . fst) $ abs
        t_fl = V.take window_size . V.dropWhile ((< start_time) . fst) $ fl
        
calcGrEl :: (V.Vector (NominalDiffTime,Double),V.Vector (NominalDiffTime,Double)) -> Maybe (Double,(Double,Double))
calcGrEl (abs,fl) = do
    let start_time = max (fst . V.head $ abs) (fst . V.head $ fl)
    let (t_abs,t_fl) = commonBegining (abs,fl)
    if V.length t_abs < window_size then Nothing else Just ()
    if V.length t_fl < window_size then Nothing else Just ()
    abs_approx <- modCalcExpFit linearRegression . V.map (\(x,y) -> (realToFrac x,y)) $ V.drop 5 t_abs
    trace (show abs_approx) Just ()
    fl_approx <- modCalcExpFit linearRegression . V.map (\(x,y) -> (realToFrac x,y)) $ V.drop 5 t_fl
    trace (show fl_approx) Just ()
    let gr = snd abs_approx
    pav <- pa abs_approx fl_approx start_time (realToFrac 7200)
    pev <- pe abs_approx fl_approx start_time (realToFrac 7200)
    return (gr,(pav,pev))

normalizeMod :: (ColonySample a) => (a RawMeasurement,a RawMeasurement) -> Maybe (V.Vector (NominalDiffTime,Double))
normalizeMod (bl,mes) = do
    let th = thresholdFromBlank bl
    let bbg = bgVal . backgroundFromBlank $ bl
    let bounds = ((0.5*) &&& (1.5*)) bbg
    bg <- backgroundFromInitMod bounds mes
    let res = V.map (\(x,y) -> (x,nmVal y)) . trim . snd . absoluteToRelativeTime . measurements . normalize bg th $ mes
    -- trace (show . trim . snd . absoluteToRelativeTime . measurements . normalize bg th $ mes) (Just ())
    if V.null res then Nothing else Just res 

generateData :: [Char] -> [Int] -> IO [[((RawAbsorbance,RawAbsorbance),(RawFluorescence,RawFluorescence))]]
generateData rows plates = do
    sequence (zipWith ($) (map generateStrainData rows) (repeat plates))

generateStrainData :: Char -> [Int] -> IO [((RawAbsorbance,RawAbsorbance),(RawFluorescence,RawFluorescence))]
generateStrainData row plates = do
    blank_abs <- sequence $ zipWith ($) (repeat $ get_abs blankWell) plates
    blank_fl <- sequence $ zipWith ($) (repeat $ get_fls blankWell) plates
    mes_abs <- mapM sequence $ zipWith (zipWith ($)) (repeat . map get_abs $ (wells row)) (map repeat plates)
    mes_fl <- mapM sequence $ zipWith (zipWith ($)) (repeat . map get_fls $ (wells row)) (map repeat plates)
    let all_abs = zipWith zip (map repeat blank_abs) mes_abs
    let all_fl = zipWith zip (map repeat blank_fl) mes_fl
    return $ concat $ zipWith zip all_abs all_fl

blankWell = Well 'e' 1

wells row = map (Well row) [1..12]

rows = ['c'] -- ['a'..'d'] ++ ['f'..'h']

plates = [0..5]

pairMaybe :: (Maybe a,Maybe b) -> Maybe (a,b)
pairMaybe (Nothing,_) = Nothing
pairMaybe (_,Nothing) = Nothing
pairMaybe (Just x,Just y) = Just (x,y)

main = do
    args <- getArgs
    let file_name_prefix = args !! 0

    raw_od_fl_with_blanks <- generateData rows plates

    let normalized_od_fl = map (map (normalizeMod *** normalizeMod)) raw_od_fl_with_blanks
    {- let concatted_od = map fst $ concat . map (map commonBegining . catMaybes . map pairMaybe) $ normalized_od_fl
    let concatted_fl = map snd $ concat . map (map commonBegining . catMaybes . map pairMaybe) $ normalized_od_fl
    let odpl_data = map (\x -> (map (show . (/3600) . realToFrac) . V.toList . V.map fst $ x,map show . V.toList . V.map (logBase 2 . snd) $ x)) $ concatted_od
    let odpl_list = concatMap pairToList odpl_data
    writeFile "test1.csv" $ printCSV odpl_list
    let flpl_data = map (\x -> (map (show . (/3600) . realToFrac) . V.toList . V.map fst $ x,map show . V.toList . V.map (logBase 2 . snd) $ x)) $ concatted_fl
    let flpl_list = concatMap pairToList flpl_data
    writeFile "test2.csv" $ printCSV flpl_list -}
    
    let elgr_data = map (map calcGrEl) . map (catMaybes . map pairMaybe) $ normalized_od_fl
    let elgr_indexed_data = zip [1..] . map catMaybes $ elgr_data
    mapM (\(x,y) -> writeFile (file_name_prefix ++ (show x) ++ "1.csv") $ printCSV [map (show . (*3600) . fst) $ y,map (show . fst . snd) $ y]) elgr_indexed_data
    mapM (\(x,y) -> writeFile (file_name_prefix ++ (show x) ++ "2.csv") $ printCSV [map (show . (*3600) . fst) $ y,map (show . snd . snd) $ y]) elgr_indexed_data

    return ()

window_size = 10

linspace :: (Fractional a, Enum a) => Int -> (a,a) -> [a]
linspace len (start,end) = take len $ [start,start+interval..end]
    where
        interval = end - start / realToFrac len

pa :: (Double,Double) -> (Double,Double) -> NominalDiffTime -> NominalDiffTime -> Maybe Double
pa (abs_a,abs_b) (fl_a,fl_b) start length = Just $ (fl (start + length) - fl (start))/(sum . map abs . linspace 10 $ (start,start+length))
    where
        abs t = 2 ** (abs_a + (realToFrac t)*abs_b)
        fl t = 2 ** (fl_a + (realToFrac t)*fl_b)

pe :: (Double,Double) -> (Double,Double) -> NominalDiffTime -> NominalDiffTime -> Maybe Double
pe (abs_a,abs_b) (fl_a,fl_b) start length = Just $ (fl start)/(abs start)
    where
        abs t = 2 ** (abs_a + (realToFrac t)*abs_b)
        fl t = 2 ** (fl_a + (realToFrac t)*fl_b)

estimationParameters = defaultEstimationParameters {outlierFraction = 0.25}

sqb w p = SampleQuery ["2013-01-06 12:00:00"] [p] [w] -- Leeat exp

get_abs :: Well -> Int -> IO (AbsorbanceSample RawMeasurement)
get_abs w p = do
    db_conf <- dbConnectInfo "db.conf"
    mes <- loadMes db_conf (sqb w p)
    return $ (\(AbsorbanceMeasurement x) -> x) . head . filter filterAbs . snd . head $ mes

get_fls :: Well -> Int -> IO (FluorescenseSample RawMeasurement)
get_fls w p = do
    db_conf <- dbConnectInfo "db.conf"
    mes <- loadMes db_conf (sqb w p)
    return $ (\(FluorescenseMeasurement x) -> x) . head . filter (not . filterAbs) . snd . head $ mes

get_fls2 :: Well -> Int -> IO (FluorescenseSample RawMeasurement)
get_fls2 w p = do
    db_conf <- dbConnectInfo "db.conf"
    mes <- loadMes db_conf (sqb w p)
    return $ (\(FluorescenseMeasurement x) -> x) . head . tail . filter (not . filterAbs) . snd . head $ mes

filterAbs (AbsorbanceMeasurement _) = True
filterAbs _ = False

modCalcExpFit :: (U.Vector Double -> U.Vector Double -> (Double,Double)) -> V.Vector (Double,Double) -> Maybe (Double,Double)
modCalcExpFit fit xys = gr . fit xs $ U.map (logBase 2) ys
    where
        (xs,ys) = U.unzip . U.fromList . V.toList $ xys
        gr (x,y) = if y <=0 then Nothing else Just (x,y)
