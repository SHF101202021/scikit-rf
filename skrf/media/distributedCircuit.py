"""
distributedCircuit (:mod:`skrf.media.distributedCircuit`)
============================================================

A transmission line mode defined in terms of distributed impedance and admittance values.

.. autosummary::
   :toctree: generated/

   DistributedCircuit

"""

from typing import TYPE_CHECKING, Union

from numpy import imag, real, sqrt

from ..constants import NumberLike
from .media import DefinedGammaZ0, Media

if TYPE_CHECKING:
    from ..frequency import Frequency


class DistributedCircuit(Media):
    r"""
    A transmission line mode defined in terms of distributed impedance and admittance values.

    Parameters
    ------------
    frequency : :class:`~skrf.frequency.Frequency` object
        frequency band of the media
    z0_port : number, array-like, or None
        `z0_port` is the port impedance for networks generated by the media.
        If `z0_port` is not None, the networks generated by the media are
        renormalized (or in other words embedded) from the characteristic
        impedance z0 of the media to `z0_port`.
        Else if `z0_port` is None, the networks port impedances will be the raw
        characteristic impedance z0 of the media.
        (Default is None)
    z0_override : number, array-like, or None
        `z0_override` override the characteristic impedance for the media.
        If `z0_override` is not None, the networks generated by the media have
        their characteristic impedance `z0` overrided by `z0_override`.
        (Default is None)
    z0 : number, array-like, or None
        deprecated parameter, alias to `z0_override` if `z0_override` is None.
        Emmit a deprecation warning.
    C : number, or array-like
            distributed capacitance, in F/m
    L : number, or array-like
            distributed inductance, in H/m
    R : number, or array-like
            distributed resistance, in Ohm/m
    G : number, or array-like
            distributed conductance, in S/m


    Notes
    -----
    if C,I,R,G are vectors they should be the same length

    :class:`DistributedCircuit` is `Media` object representing a
    transmission line mode defined in terms of distributed impedance
    and admittance values.

    A `DistributedCircuit` may be defined in terms
    of the following attributes:

    ================================  ================  ================
    Quantity                          Symbol            Property
    ================================  ================  ================
    Distributed Capacitance           :math:`C^{'}`     :attr:`C`
    Distributed Inductance            :math:`L^{'}`     :attr:`L`
    Distributed Resistance            :math:`R^{'}`     :attr:`R`
    Distributed Conductance           :math:`G^{'}`     :attr:`G`
    ================================  ================  ================


    The following quantities may be calculated, which are functions of
    angular frequency (:math:`\omega`):

    ===================================  ==================================================  ========================
    Quantity                             Symbol                                              Property
    ===================================  ==================================================  ========================
    Distributed Impedance                :math:`Z^{'} = R^{'} + j \omega L^{'}`              :attr:`Z`
    Distributed Admittance               :math:`Y^{'} = G^{'} + j \omega C^{'}`              :attr:`Y`
    ===================================  ==================================================  ========================


    The properties which define their wave behavior:

    ===================================  ============================================  ==============================
    Quantity                             Symbol                                        Method
    ===================================  ============================================  ==============================
    Characteristic Impedance             :math:`Z_0 = \sqrt{ \frac{Z^{'}}{Y^{'}}}`     :func:`Z0`
    Propagation Constant                 :math:`\gamma = \sqrt{ Z^{'}  Y^{'}}`         :func:`gamma`
    ===================================  ============================================  ==============================

    Given the following definitions, the components of propagation
    constant are interpreted as follows:

    .. math::

        +\Re e\{\gamma\} = \text{attenuation}

        -\Im m\{\gamma\} = \text{forward propagation}


    See Also
    --------
    from_media

    """

    def __init__(self, frequency: Union['Frequency', None] = None,
                 z0_port: Union[NumberLike, None] = None,
                 z0_override: Union[NumberLike, None] = None,
                 z0: Union[NumberLike, None] = None,
                 C: NumberLike = 90e-12, L: NumberLike = 280e-9,
                 R: NumberLike = 0, G: NumberLike = 0,
                *args, **kwargs):
        Media.__init__(self, frequency = frequency,
                       z0_port = z0_port, z0_override = z0_override, z0 = z0)

        self.C, self.L, self.R, self.G = C,L,R,G


    def __str__(self) -> str:
        f=self.frequency
        try:
            output = (
                f'Distributed Circuit Media.  {f.f_scaled[0]}-{f.f_scaled[-1]} {f.unit}.  {f.npoints} points'
                f'\nL\'= {self.L:.2f}, C\'= {self.C:.2f},R\'= {self.R:.2f}, G\'= {self.G:.2f}, ')
        except(TypeError):
            output = (
                f'Distributed Circuit Media.  {f.f_scaled[0]}-{f.f_scaled[-1]} {f.unit}.  {f.npoints} points'
                f'\nL\'= {self.L:.2f}.., C\'= {self.C:.2f}..,R\'= {self.R:.2f}.., G\'= {self.G:.2f}.., ')
        return output

    def __repr__(self) -> str:
        return self.__str__()

    @classmethod
    def from_media(cls, my_media: Media, *args, **kwargs) -> Media:
        """
        Initializes a `DistributedCircuit` from an existing
        :class:`~skrf.media.media.Media` instance.

        Parameters
        ----------
        my_media : :class:`~skrf.media.media.Media` instance.
            the media object

        See Also
        --------
        :class:`~skrf.media.media.Media`
        """

        w  =  my_media.frequency.w
        gamma = my_media.gamma
        z0 = my_media.z0
        z0_port = my_media.z0_port

        Y = gamma/z0
        Z = gamma*z0
        G,C = real(Y), imag(Y)/w
        R,L = real(Z), imag(Z)/w
        return cls(frequency = my_media.frequency,
                   z0_port = z0_port, C=C, L=L, R=R, G=G, *args, **kwargs)

    @classmethod
    def from_csv(self, *args, **kw):
        """
        Create a `DistributedCircuit` from numerical values stored in a csv file.

        The csv file format must be written by the function :func:`write_csv`,
        or similar method which produces the following format::

            f[$unit], Re(z0), Im(z0), Re(gamma), Im(gamma), Re(z0_port), Im(z0_port)
            1, 1, 1, 1, 1, 1, 1
            2, 1, 1, 1, 1, 1, 1
            .....

        See Also
        --------
        write_csv
        """
        d = DefinedGammaZ0.from_csv(*args,**kw)
        return self.from_media(d)

    @property
    def Z(self) -> NumberLike:
        r"""
        Distributed Impedance, :math:`Z^{'}`.

        Defined as

        .. math::

                Z^{'} = R^{'} + j \omega L^{'}

        Returns
        -------
        Z : npy.ndarray
            Distributed impedance in units of ohm/m
        """
        w  = self.frequency.w
        Z = self.R + 1j*w*self.L
        # Avoid divide by zero.
        # Needs to be imaginary to avoid all divide by zeros in the media class.
        Z[Z.imag == 0] += 1j*1e-12
        return Z

    @property
    def Y(self) -> NumberLike:
        r"""
        Distributed Admittance, :math:`Y^{'}`.

        Defined as

        .. math::

                Y^{'} = G^{'} + j \omega C^{'}

        Returns
        -------
        Y : npy.ndarray
            Distributed Admittance in units of S/m
        """

        w  = self.frequency.w
        Y = self.G + 1j*w*self.C
        # Avoid divide by zero.
        # Needs to be imaginary to avoid all divide by zeros in the media class.
        Y[Y.imag == 0] += 1j*1e-12
        return Y

    @property
    def z0_characteristic(self) -> NumberLike:
        r"""
        Characteristic Impedance, :math:`z_0`

        .. math::

                Z_0 = \sqrt{ \frac{Z^{'}}{Y^{'}}}

        Returns
        -------
        z0_characteristic : npy.ndarray
            Characteristic Impedance in units of ohms
        """
        return sqrt(self.Z/self.Y)

    @property
    def gamma(self) -> NumberLike:
        r"""
        Propagation Constant, :math:`\gamma`.

        Defined as,

        .. math::

                \gamma =  \sqrt{ Z^{'}  Y^{'}}

        Returns
        -------
        gamma : npy.ndarray
                Propagation Constant,

        Note
        ----
        The components of propagation constant are interpreted as follows:

        * positive real(gamma) = attenuation
        * positive imag(gamma) = forward propagation
        """
        return sqrt(self.Z*self.Y)
