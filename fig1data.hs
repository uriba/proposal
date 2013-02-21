import Biolab.Interfaces.MySql
import Biolab.Analysis.GrowthRate
import Biolab.Analysis.Utils
import Biolab.Analysis.Normalization
import Biolab.Types
import Biolab.Analysis.Types
import Data.Map ((!))
import Data.Maybe (fromJust, isJust, catMaybes)
import qualified Data.Map as M
import qualified Data.Vector as V
import Data.Time (UTCTime, NominalDiffTime)
import Text.CSV

dataToUse = (well,experiments,plates)
    where
        well = [Well 'a' 4]
        experiments = ["2013-02-12 13:46:13"]
        plates = [0]

main = do
    db_conf <- dbConnectInfo "db.conf"
    let (wells,experiments,plates) = dataToUse
    let sq = SampleQuery experiments plates wells
    mes <- loadMes db_conf sq
    let abs_mes = (\(AbsorbanceMeasurement x) -> asMes x) . head . filter filterAbs . snd . head $ mes
    let rel_raw = snd . absoluteToRelativeTime $ abs_mes
    let times = map ( show . (/3600) . realToFrac ) . V.toList . V.map fst $ rel_raw
    let vals = map (show . mVal) . V.toList . V.map snd $ rel_raw
    let graph1 = [times,vals]
    writeFile "graph1.csv" $ printCSV graph1
    return ()

mvToV :: V.Vector (NominalDiffTime, Maybe NominalDiffTime) -> Maybe (V.Vector (Double,Double))
mvToV v
    | V.null real_vals= Nothing
    | otherwise = Just $ V.map (\(x,y) -> ((/3600) . realToFrac $ x, (/3600) . realToFrac . fromJust $ y)) real_vals
    where real_vals = V.filter (isJust . snd) v

rmToV :: (ColonySample a) => a RawMeasurement -> V.Vector (Double,Double)
rmToV = V.map (\(x,y) -> ((/3600) . realToFrac $ x,mVal y)) . trim . snd . absoluteToRelativeTime . measurements

nmToV :: (ColonySample a) => a NormalizedMeasurement -> V.Vector (Double,Double)
nmToV = V.map (\(x,y) -> ((/3600) . realToFrac $ x,logBase 2 . nmVal $ y)) . trim . snd . absoluteToRelativeTime . measurements

getGrs :: (ColonySample a) => [(SampleId, a RawMeasurement)] -> [(SampleId, a RawMeasurement)] -> [(SampleId, (V.Vector (NominalDiffTime,Maybe NominalDiffTime), a RawMeasurement, a NormalizedMeasurement))]
getGrs blanks cultures = map (\(sid,v) -> (sid, (doublingTime (Just 9) {- Nothing -} . normed sid $ v,v, normed sid v))) cultures
    where
        bgs sid = backgroundFromBlanks (blankValsOf sid $ blanks) :: Background
        thds sid = (thresholdFromBlanks (blankValsOf sid $ blanks)) :: DetectionThreshold
        normed sid = normalize (bgs sid) (thds sid)


getAbsorbance = map (\(sid,mes) -> (sid, (\(AbsorbanceMeasurement x) -> x) . head $ filter filterAbs mes))
getFluorescence = map (\(sid,mes) -> (sid, (\(FluorescenseMeasurement x) -> x) . head $ filter filterFls mes))
getFluorescence2 = map (\(sid,mes) -> (sid, (\(FluorescenseMeasurement x) -> x) . head . tail $ filter filterFls mes))

filterFls (FluorescenseMeasurement _) = True
filterFls _ = False

filterAbs (AbsorbanceMeasurement _) = True
filterAbs _ = False

blanksOf :: SampleId -> [(SampleId,a)] -> [(SampleId,a)]
blanksOf sid = filter (\(sid2,_) -> sidExpId sid == sidExpId sid2 && sidPlate sid == sidPlate sid2)

blankValsOf :: (ColonySample a) => SampleId -> [(SampleId,a RawMeasurement)] -> [a RawMeasurement]
blankValsOf sid = map snd . blanksOf sid
