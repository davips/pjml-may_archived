import traceback
import numpy

class ExceptionHandler:
    """Handle transformer exceptions and enable/disable numpy warnings.

        E.g. Mahalanobis distance in KNN needs to supress warnings due to NaN
        in linear algebra calculations. MLP is also verbose due to
        nonconvergence issues among other problems.
    """
    name = None

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
              f'Transformer: {self.name}...\n')
        if not any([str(e).__contains__(msg) for msg in self.msgs]):

            # HINTS
            if str(e).__contains__('cannot perform reduce with flexible type'):
                from pjml.tool.data.processing.feature.binarize import Binarize
                print(f'HINT: your pipeline may be missing a '
                      f'{Binarize.name} component')

            # end of handling
            if exit_on_error:
                traceback.print_exc()
                exit(0)
            else:
                raise e
        else:
            print(' just a known pipeline failure.'
                  'Will be put onto Data object.')


# class ComponentException(Exception):
#     pass


class MissingModel(Exception):
    pass


class BadComponent(Exception):
    pass
