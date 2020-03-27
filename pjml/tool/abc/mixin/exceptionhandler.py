import traceback
from abc import abstractmethod

import numpy

from pjdata.data import NoData


class ExceptionHandler:
    """Handle transformer exceptions and enable/disable numpy warnings.

        E.g. Mahalanobis distance in KNN needs to supress warnings due to NaN
        in linear algebra calculations. MLP is also verbose due to
        nonconvergence issues among other problems.
    """
    @classmethod
    @abstractmethod
    def name(cls):
        pass

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
            'subtransformer failed',  # nested failure
            'specified nu is infeasible',  # SVM
            'excess of neurons',
            ]
    transformer = None

    def _handle_exception(self, e, exit_on_error):
        """Pipeline failure is different from python error."""
        print(f'At {self},\nTrying to handle:\n[{str(e)}]\n'
              f'Object: {self.name}...\n')
        if not any([str(e).__contains__(msg) for msg in self.msgs]):

            # HINTS
            if str(e).__contains__('cannot perform reduce with flexible type') \
                    or str(e).__contains__('could not convert string to float'):
                from pjml.tool.data.processing.feature.binarize import Binarize
                print(f'HINT: your pipeline may be missing a '
                      f'{Binarize.name} component')

            # end of handling
            print('TODO: is exit_on_error implemented? exit_on_error=', exit_on_error)
            # if exit_on_error:
            #     traceback.print_exc()
            #     exit(0)
            # else:
            raise e
        else:
            print(' just a known pipeline failure.'
                  'Will be put onto Data object.')

    def _check_nodata(self, data):
        from pjml.tool.abc.mixin.nodatahandler import NoDataHandler
        if data is NoData and not isinstance(self, NoDataHandler):
            raise Exception(f'NoData is not accepted by {self.name}!')


class MissingModel(Exception):
    pass


class BadComponent(Exception):
    pass
