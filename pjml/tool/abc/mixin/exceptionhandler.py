import traceback
from abc import abstractmethod

import numpy

from pjdata.aux.decorator import classproperty
from pjdata.history import History


class ExceptionHandler:
    """Handle transformer exceptions and enable/disable numpy warnings.

        E.g. Mahalanobis distance in KNN needs to supress warnings due to NaN
        in linear algebra calculations. MLP is also verbose due to
        nonconvergence issues among other problems.
    """

    @classproperty
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
        if isinstance(self.name, str):
            print(
                f'At {self},\nTrying to handle:\n[{str(e)}]\nObject: '
                f'{self.name}...\n')
        else:
            print(
                f'At {self},\nTrying to handle:\n[{str(e)}]\nObject: '
                f'{self.name()}...\n')
        if not any([str(e).__contains__(msg) for msg in self.msgs]):

            # HINTS
            if str(e).__contains__('cannot perform reduce with flexible type') \
                    or str(e).__contains__('could not convert string to float'):
                from pjml.tool.data.processing.feature.binarize import Binarize
                print(f'HINT: your pipeline may be missing a '
                      f'{Binarize.name} component')

            # end of handling
            # print('TODO: is exit_on_error implemented? exit_on_error=',
            #       exit_on_error)
            # if exit_on_error:
            #     traceback.print_exc()
            #     print('Exiting...')
            #     exit(0)
            # else:
            raise e
        else:
            print(' just a known pipeline failure.'
                  'Will be put onto Data object.')

    def _check_nodata(self, data, transformer):
        from pjdata.specialdata import NoData
        if data is NoData and not transformer.nodata_handler:
            raise Exception(f'NoData is not accepted by {self.name}!')

    def _check_history(self, datain, dataout, transformations):
        """Check consistency between resulting Data object and
        _transformations() implementation provided by the current
        component."""
        from pjdata.specialdata import NoData
        if dataout is NoData or dataout is None:
            return dataout

        recent = dataout.history.transformations[datain.history.size:]
        transfs = transformations

        if History(recent).id != History(transfs).id:
            print('\nTransformed Data object recent history:::::::::::::::::\n'
                  f'{recent}\n'
                  f'Expected transformations::::::::::::::::::::::::::::::::\n'
                  f'{transfs}\n'
                  'Transformed Data object history does not '
                  'match expected transformation list.\n'
                  'Please override self._transformations() '
                  f'method for {self.name} or extend a proper parent class '
                  f'like \'Invisible\'.')
            raise BadComponent(f'Inconsistent Data object history!')

        return dataout


class MissingModel(Exception):
    pass


class BadComponent(Exception):
    pass

# import traceback
# from abc import abstractmethod
#
# import numpy
#
# from pjdata.aux.decorator import classproperty
# from pjdata.data import NoData
#
#
# class ExceptionHandler:
#     """Handle transformer exceptions and enable/disable numpy warnings.
#
#         E.g. Mahalanobis distance in KNN needs to supress warnings due to NaN
#         in linear algebra calculations. MLP is also verbose due to
#         nonconvergence issues among other problems.
#     """
#
#     @classproperty
#     @abstractmethod
#     def name(cls):
#         pass
#
#     @staticmethod
#     def _handle_warnings():
#         numpy.warnings.filterwarnings('ignore')
#
#     @staticmethod
#     def _dishandle_warnings():
#         numpy.warnings.filterwarnings('always')
#
#     msgs = ['All features are either constant or ignored.',  # CB
#             'be between 0 and min(n_samples, n_features)',  # DR*
#             'excess of max_free_parameters:',  # MLP
#             'Timed out!',
#             'Mahalanobis for too big data',
#             'MemoryError',
#             'On entry to DLASCL parameter number',  # Mahala knn
#             'excess of neighbors!',  # KNN
#             'subtransformer failed',  # nested failure
#             'specified nu is infeasible',  # SVM
#             'excess of neurons',
#             'could not convert string to float',
#             f'HINT: your pipeline may be missing a '
#             f'{Binarize.name} component'  # missing Binarize
#             'cannot perform reduce with flexible type'
#             ]
#
#     transformer = None
#
#     def _handle_exception(self, e, exit_on_error):
#         """Pipeline failure is different from python error."""
#         if isinstance(self.name, str):
#             print(
#                 f'At {self},\nTrying to handle:\n[{str(e)}]\nObject: '
#                 f'{self.name}...\n')
#         else:
#             print(
#                 f'At {self},\nTrying to handle:\n[{str(e)}]\nObject: '
#                 f'{self.name()}...\n')
#         filtered = {msg: str(e).__contains__(msg) for msg in self.msgs}
#         if not any(filtered):
#             # end of handling
#             print('TODO: is exit_on_error implemented? exit_on_error=',
#                   exit_on_error)
#             # if exit_on_error:
#             #     traceback.print_exc()
#             #     exit(0)
#             # else:
#             raise e
#         else:
#             print(' just a known pipeline failure.'
#                   'Will be put onto Data object.')
#             print('HINT: ', self.msgs[msg])
#
#     def _check_nodata(self, data):
#         from pjml.tool.abc.mixin.nodatahandler import NoDataHandler
#         if data is NoData and not isinstance(self, NoDataHandler):
#             raise Exception(f'NoData is not accepted by {self.name}!')
#
#
# class MissingModel(Exception):
#     pass
#
#
# class BadComponent(Exception):
#     pass
