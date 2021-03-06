import abc

import flywheel

from custom_curator.utils import Container


class Curator(abc.ABC):
    """An abstract class that user-defined Curator class should inherited from.

    This class defines abstract methods for each container type (e.g. `curate_project`)
    (i.e. methods that need to be defined in the child curator Class implemented by the
    user, see example scripts in the example folder). Such method is decorated with
    the `abc.abstractmethod` decorator in this abstract class. Validation methods
    are also defined for each container types. Validation methods become handy
    when, for example, curating a file is a time consuming process: it allows
    for marking a file during the curation method and check for that mark elsewhere in
    the validate method.

    Example:
    >>> from custom_curator import curator
    >>> class Curator(curator.Curator):
    ...
    ...     def curate_file(self, file_):
    ...	       # Curates a file by setting the field 'file.info.curated' to True
    ...	       file_.update_info({'curated': True})
    ...
    ...     def validate_file(self, file_):
    ...	        # Returns True if file needs curation, False otherwise
    ...     	return not file_.info.get('curated', False)
    """

    def __init__(self, depth_first=True):
        """An abstract class to be implemented in the input python file."""
        self.depth_first = depth_first
        self.input_file_one = None
        self.input_file_two = None
        self.input_file_three = None
        self.context = None
        self.client = None

    def curate_container(self, container: Container):
        """Curates a generic container.

        Args:
            container (Container): A Flywheel container.
        """
        if hasattr(container, "container_type"):
            container_type = container.container_type
            if container_type == "project":
                if self.validate_project(container):
                    self.curate_project(container)
            elif container_type == "subject":
                if self.validate_subject(container):
                    self.curate_subject(container)
            elif container_type == "session":
                if self.validate_session(container):
                    self.curate_session(container)
            elif container_type == "acquisition":
                if self.validate_acquisition(container):
                    self.curate_acquisition(container)
            elif container_type == "file":
                if self.validate_file(container):
                    self.curate_file(container)
            else:
                if self.validate_analysis(container):
                    self.curate_analysis(container)
        else:
            # element is a file and has no children
            if self.validate_file(container):
                self.curate_file(container)

    @abc.abstractmethod
    def curate_project(self, project: flywheel.Project):
        """Curates a project.

        Args:
            project (flywheel.Project): The project object to curate
        """
        raise NotImplementedError

    @abc.abstractmethod
    def curate_subject(self, subject: flywheel.Subject):
        """Curates a subject.

        Args:
            subject (flywheel.Subject): The subject object to curate
        """
        raise NotImplementedError

    @abc.abstractmethod
    def curate_session(self, session: flywheel.Session):
        """Curates a session.

        Args:
            session (flywheel.Session): The session object to curate
        """
        raise NotImplementedError

    @abc.abstractmethod
    def curate_acquisition(self, acquisition: flywheel.Acquisition):
        """Curates an acquisition.

        Args:
            acquisition (flywheel.Acquisition): The acquisition object to
                curate
        """
        raise NotImplementedError

    @abc.abstractmethod
    def curate_analysis(self, analysis: flywheel.AnalysisOutput):
        """Curates an analysis.

        Args:
            analysis (flywheel.Analysis): The analysis object to curate
        """
        raise NotImplementedError

    @abc.abstractmethod
    def curate_file(self, file_: flywheel.FileEntry):
        """Curates a file.

        Args:
            file_ (flywheel.FileEntry): The file entry object to curate
        """
        raise NotImplementedError

    def validate_project(self, project: flywheel.Project):
        """Returns True if a project needs curation, False otherwise.

        Args:
            project (flywheel.Project): The project object to validate

        Returns:
            bool: Whether or not the project is curated correctly
        """
        return True

    def validate_subject(self, subject: flywheel.Subject):
        """Returns True if a subject needs curation, False otherwise.

        Args:
            subject (flywheel.Subject): The subject object to validate

        Returns:
            bool: Whether or not the subject is curated correctly
        """
        return True

    def validate_session(self, session: flywheel.Session):
        """Returns True if a session needs curation, False otherwise.

        Args:
            session (flywheel.Session): The session object to validate

        Returns:
            bool: Whether or not the session is curated correctly
        """
        return True

    def validate_acquisition(self, acquisition: flywheel.Acquisition):
        """Returns True if a acquisition needs curation, False otherwise.

        Args:
            acquisition (flywheel.Acquisition): The acquisition object to
                validate

        Returns:
            bool: Whether or not the acquisition is curated correctly
        """
        return True

    def validate_analysis(self, analysis: flywheel.AnalysisOutput):
        """Returns True if a analysis needs curation, False otherwise.

        Args:
            analysis (flywheel.Analysis): The analysis object to validate

        Returns:
            bool: Whether or not the analysis is curated correctly
        """
        return True

    def validate_file(self, file_: flywheel.FileEntry):
        """Returns True if a file_ needs curation, False otherwise.

        Args:
            file_ (flywheel.FileEntry): The file entry object to validate

        Returns:
            bool: Whether or not the file_ is curated correctly
        """
        return True
