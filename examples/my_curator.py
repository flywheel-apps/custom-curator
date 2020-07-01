"""
An example curation script to correct the session.label based on a predefined
mapping and the classification based on the Dicom SeriesDescription data element.
"""

import json
import logging

import flywheel
from flywheel_gear_toolkit import GearToolkitContext

from custom_curator import curator
from custom_curator.reporters import CuratorErrorReporter


log = logging.getLogger("my_curator")
log.setLevel("DEBUG")

SESSION_LABEL_CORRECTION = {
    "screening": "Screening",
    "w04": "Week_04",
    "w12": "Week_12",
    "w16": "Week_16",
    "w20": "Week_20",
    "w24": "Week_24",
    "w28": "Week_28",
    "w36": "Week_36",
    "w48": "Week_48",
    "REV1": "Relapse_Evaluation_1",
}


class Curator(curator.Curator):
    def __init__(self):
        super(Curator, self).__init__(depth_first=True)

    def curate_project(self, project: flywheel.Project):
        gear_context = GearToolkitContext()
        self.error_reporter = CuratorErrorReporter(
            output_dir=gear_context.output_dir, project_label=project.label
        )
        log.debug("Curating project with %s", self.input_file_one)
        if self.input_file_one:
            with open(self.input_file_one, "r") as fp:
                updates = json.load(fp)
            log.debug("Updates are %s", updates)
            project.update(updates)

    def curate_subject(self, subject: flywheel.Subject):
        pass

    def curate_session(self, session: flywheel.Session):
        log.info("Curating session %s", session.id)
        try:
            new_label = SESSION_LABEL_CORRECTION.get(session.label)
            if new_label:
                session.update({"label": new_label})
        except Exception as exc:
            self.error_reporter.write_file_error(
                errors_list=[],
                err_str=str(exc),
                subject_label=session.subject.id,
                subject_id=session.subject.id,
                session_label=session.label,
                session_id=session.id,
                acquisition_label="",
                acquisition_id="",
                file_name="",
                resolved="False",
                search_key="",
            )

    def curate_acquisition(self, acquisition: flywheel.Acquisition):
        acquisition.update_info({"Harsha": 10})

    def curate_analysis(self, analysis):
        pass

    def curate_file(self, file_: flywheel.FileEntry):
        log.info("Curating file %s", file_.name)
        try:
            new_classification = self.classify_file(file_)
            if new_classification is None:
                return
            else:
                log.debug(
                    "file %s classification updated to %s",
                    file_.name,
                    new_classification,
                )
                file_.update_classification(new_classification)
        except Exception as exc:
            ref = file_._parent.ref()
            kwargs = {f"{ref.type}_id": ref["id"]}
            self.error_reporter.write_file_error(
                errors_list=[],
                err_str=str(exc),
                file_name=file_.name,
                resolved="False",
                search_key="",
                **kwargs,
            )

    @staticmethod
    def classify_file(file_: flywheel.FileEntry):
        series_description = file_.info.get("SeriesDescription")
        classification = file_.classification
        if "a_special_string" in series_description.lower():
            classification["Custom"].append("HasSpecialString")
            return classification
        return None
