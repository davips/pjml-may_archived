from pjml.tool.base.component import Component


class Sampler(Component):
    """Class to perform, e.g. Expand+kfoldCV.

    This task is already done by function sampler,
    but if performance becomes a concern, this less modular solution is a
    good choice."""
