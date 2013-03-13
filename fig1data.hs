import Biolab.Interfaces.MySql
import Biolab.Analysis.GrowthRate
import Biolab.Analysis.Utils
import Biolab.Analysis.Normalization
import Biolab.Types
import Biolab.Analysis.Types
import qualified Data.Vector as V
import Data.Time (UTCTime, NominalDiffTime)
import Text.CSV
import System.Environment (getArgs)

main = do
    args <- getArgs
    let file_name_prefix = args !! 0
    abs_mes <- get_abs (Well 'e' 8)
    -- abs_mes <- get_abs (Well 'd' 6)
    let times = getTimesFromUtc . asMes $ abs_mes
    let vals = map (show . mVal) . V.toList . V.map snd $ asMes abs_mes
    writeFile (file_name_prefix ++ "1.csv") $ printCSV [times,vals]

    abs_blk <- get_abs (Well 'h' 12)
    -- abs_blk <- get_abs (Well 'e' 1)
    let threshold = thresholdFromBlank abs_blk
    let normalized = normalizeFromInit abs_mes
    let trimmed_mes = trim . snd . absoluteToRelativeTime . asMes $ normalized
    let trimmed_times = getTimes trimmed_mes

    let trimmed_vals = map (show . nmVal) . V.toList . V.map snd $ trimmed_mes
    writeFile (file_name_prefix ++ "2.csv") $ printCSV [trimmed_times, trimmed_vals]

    let trimmed_log_vals = map (show . logBase 2 . nmVal) . V.toList . V.map snd $ trimmed_mes
    writeFile (file_name_prefix ++ "3.csv") $ printCSV [trimmed_times,trimmed_log_vals]

    let dts = V.map (\(x,Just y) -> (x,y)) . V.filter (not . (== Nothing) . snd) . growthRate (Just 18) $ normalized
    let dt_times = getTimes dts
    let dt_vals = map (show . (*3600)) . V.toList . V.map snd $ dts
    writeFile (file_name_prefix ++ "4.csv") $ printCSV [dt_times,dt_vals]
    return ()

get_abs :: Well -> IO (AbsorbanceSample RawMeasurement)
get_abs w = do
    db_conf <- dbConnectInfo "db.conf"
    let sqb = SampleQuery ["2013-02-12 13:46:13"] [0] [w]
    -- let sqb = SampleQuery ["2013-01-06 12:00:00"] [0] [w]
    mes <- loadMes db_conf sqb
    return $ (\(AbsorbanceMeasurement x) -> x) . head . filter filterAbs . snd . head $ mes

getTimesFromUtc :: V.Vector (UTCTime,a) -> [String]
getTimesFromUtc = getTimes . snd . absoluteToRelativeTime

getTimes :: V.Vector (NominalDiffTime,a) -> [String]
getTimes ca = map ( show . (/3600) . realToFrac ) . V.toList . V.map fst $ ca

filterAbs (AbsorbanceMeasurement _) = True
filterAbs _ = False
