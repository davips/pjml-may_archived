from abc import abstractmethod

import numpy

from pjdata.aux.decorator import classproperty
from pjml.tool.abc.mixin.timers import Timers


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
            # TODO: remove the need for this IF, if it still exists
            print(f'At {self.name},\nTrying to handle:\n[{str(e)}]')
        else:
            print(f'At {self.name()},\nTrying to handle:\n[{str(e)}]')
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
        #TODO: global(?) option to disable history checking (takes 0.2ms at most)
        # st = Timers._clock()
        from pjdata.specialdata import NoData
        if dataout is NoData or dataout.isfrozen or dataout.allfrozen:
            return dataout

        # Revert all presumed transformations.
        previous_uuid = dataout.uuid00
        # print(transformations)
        # print('9999999999999999999999999999999999999999')
        for transformation in reversed(transformations):
            # TODO: catch past uuidzero subtraction and alert user of
            #  transformations in excess.
            # print('sai', previous_uuid, 'do', transformation.uuid00, transformation.name)
            previous_uuid -= transformation.uuid00
            # print('entrou', previous_uuid)
            # print()

        # Check if reverted uuid is the same as the one from original data.
        if previous_uuid != datain.uuid00:
            recent = dataout.history[len(datain.history):]
            print('\nActual history::::::::::::::: [estimated datain:',
                  previous_uuid)
            for t in recent:
                print(f'{t}')

            print(f'\nExpected history:::::::::::::::: [datain:',
                  datain.uuid00)
            for t in transformations:
                print(f'{t}')

            print(f'\nTransformed Data object history does not '
                  'match expected transformation list.\n'
                  'Please override self._transformations() '
                  f'method for {self.name} or extend a proper parent class '
                  f'like \'Invisible\'.\n')

            print('in:', type(datain), datain)
            print('out:', type(dataout), dataout)

            raise BadComponent(f'Inconsistent Data object history!')

        # print((Timers._clock() - st)*1000, 'ms')
        return dataout


class MissingModel(Exception):
    pass


class BadComponent(Exception):
    pass
