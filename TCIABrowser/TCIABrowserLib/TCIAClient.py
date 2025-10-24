import slicer, json, string, csv, urllib.request, urllib.parse, urllib.error

try:
    slicer.util.pip_install('tcia_utils -U -q')
    slicer.util.pip_install('pandas')
except:
    slicer.util.pip_install('tcia_utils')
    slicer.util.pip_install('pandas')
import tcia_utils.nbia
import pandas as pd

#import TCIABrowserLib

#
# Refer https://wiki.cancerimagingarchive.net/display/Public/TCIA+Programmatic+Interface+REST+API+Guides for the API guide
#
class TCIAClient:
    def __init__(self, apiUrl = ""):
        self.apiUrl = apiUrl

    def get_collection_values(self):
        return tcia_utils.nbia.getCollections(api_url = self.apiUrl)

    def get_collection_descriptions(self):
        return tcia_utils.nbia.getCollectionDescriptions(self.apiUrl)

    def get_patient(self, collection = None):
        return tcia_utils.nbia.getPatient(collection, api_url = self.apiUrl)

    def get_patient_study(self, collection = None, patientId = None, studyInstanceUid = None):
        return tcia_utils.nbia.getStudy(collection, patientId, studyInstanceUid, api_url = self.apiUrl)

    def get_series(self, collection = None, patientId = None, studyInstanceUID = None, seriesInstanceUID = None, modality = None,
                   bodyPartExamined = None, manufacturer = None, manufacturerModel = None):
        return tcia_utils.nbia.getSeries(collection, patientId, studyInstanceUID, seriesInstanceUID, modality,
                                         bodyPartExamined, manufacturer, manufacturerModel, api_url = self.apiUrl)

    def get_image(self, seriesInstanceUids, path):
        return tcia_utils.nbia.downloadSeries(seriesInstanceUids, input_type = 'list', api_url = self.apiUrl, path = path, as_zip = False)

    def get_seg_ref_series(self, seriesInstanceUid):
        refSeries = tcia_utils.nbia.getSegRefSeries(seriesInstanceUid, api_url = self.apiUrl)
        if not refSeries:
            return None, None
        response = tcia_utils.nbia.getSeriesList([refSeries], api_url = self.apiUrl)
        if response.empty:
            return None, None
        metadata = response.iloc[0]
        fileSize = round(int(metadata["FileSize"])/1048576, 2)
        return metadata["SeriesInstanceUID"], 0.01 if fileSize <= 0.01 else fileSize