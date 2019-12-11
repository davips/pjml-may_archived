from functools import lru_cache


class FunctionInspector:
    @property
    @lru_cache()
    def functions(self):
        """Map each function name to its corresponding class method."""
        return {name.split('_fun_')[1]: getattr(self, name)
                for name in dir(self) if '_fun' in name}
