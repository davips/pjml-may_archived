import traceback
import numpy


class ExceptionHandler:
    """Handle component exceptions and enable/disable numpy warnings.

        E.g. Mahalanobis distance in KNN needs to supress warnings due to NaN
        in linear algebra calculations. MLP is also verbose due to
        nonconvergence issues among other problems.
    """

    @staticmethod
    def _handle_warnings():
        numpy.warnings.filterwarnings('ignore')

    @staticmethod
    def _dishandle_warnings():
        numpy.warnings.filterwarnings('always')

    msgs = ['All features are either constant or ignored.',  # CB
            'be between 0 and min(n_samples, n_features)',  # DR*
            'excess of max_free_parameters:',  # MLP
            'Timed out!',
            'Mahalanobis for too big data',
            'MemoryError',
            'On entry to DLASCL parameter number',  # Mahala knn
            'excess of neighbors!',  # KNN
            'subcomponent failed',  # nested failure
            'specified nu is infeasible',  # SVM
            'excess of neurons',
            ]
    transformer = None

    def _handle_exception(self, e):
        print(f'Trying to handle: [{str(e)}] at {self.transformer}...')
        if not any([str(e).__contains__(msg) for msg in self.msgs]):
            traceback.print_exc()
            exit(0)


class ComponentException(Exception):
    pass


class NoModel(Exception):
    pass


class BadComponent(Exception):
    pass
