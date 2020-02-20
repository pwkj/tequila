from tequila.circuit import gates
from tequila.circuit.gradient import grad
from tequila.objective import ExpectationValue
from tequila.objective.objective import Variable
from tequila.hamiltonian import paulis
from tequila import simulate
from tequila import simulators
import numpy
import pytest



@pytest.mark.parametrize("simulator", [simulators.pick_backend("random"), simulators.pick_backend()])
@pytest.mark.parametrize("controlled", [False, True])
@pytest.mark.parametrize("angle_value", numpy.random.uniform(0.0, 2.0*numpy.pi, 1))
def test_gradient_UY_HX(simulator, angle_value, controlled, silent=True):
    # case X Y
    # U = cos(angle/2) + sin(-angle/2)*i*Y
    # <0|Ud H U |0> = cos^2(angle/2)*<0|X|0>
    # + sin^2(-angle/2) <0|YXY|0>
    # + cos(angle/2)*sin(angle/2)*i<0|XY|0>
    # + sin(-angle/2)*cos(angle/2)*(-i) <0|YX|0>
    # = cos^2*0 + sin^2*0 + cos*sin*i(<0|[XY,YX]|0>)
    # = 0.5*sin(-angle)*i <0|[XY,YX]|0> = -0.5*sin(angle)*i * 2 i <0|Z|0>
    # = sin(angle)

    angle = Variable(name="angle")
    variables = {angle: angle_value}

    qubit = 0
    H = paulis.X(qubit=qubit)
    if controlled:
        control = 1
        U = gates.X(target=control) + gates.Ry(target=qubit, control=control, angle=angle)
    else:
        U = gates.X(target=qubit) + gates.X(target=qubit)  + gates.Ry(target=qubit, angle=angle)
    O = ExpectationValue(U=U, H=H)
    E = simulate(O, variables=variables, backend=simulator)
    print("O={type}".format(type=type(O)))
    dO = grad(objective=O, variable=angle)
    dE = simulate(dO, variables=variables, backend=simulator)
    assert (numpy.isclose(E, numpy.sin(angle(variables)), atol=1.e-4))
    assert (numpy.isclose(dE, numpy.cos(angle(variables)), atol=1.e-4))
    if not silent:
        print("E         =", E)
        print("sin(angle)=", numpy.sin(angle()))
        print("dE        =", dE)
        print("cos(angle)=", numpy.cos(angle()))


@pytest.mark.parametrize("simulator", [simulators.pick_backend("random"), simulators.pick_backend()])
@pytest.mark.parametrize("controlled", [False, True])
@pytest.mark.parametrize("angle_value", numpy.random.uniform(0.0, 2.0*numpy.pi, 1))
def test_gradient_UX_HY(simulator, angle_value, controlled, silent=False):
    # case YX
    # U = cos(angle/2) + sin(-angle/2)*i*X
    # O = cos*sin*i*<0|YX|0> + sin*cos*(-i)<0|XY|0>
    #   = 0.5*sin(-angle)*i <0|[YX,XY]|0>
    #   = -sin(angle)

    angle = Variable(name="angle")
    variables = {angle: angle_value}

    qubit = 0
    H = paulis.Y(qubit=qubit)
    if controlled:
        control = 1
        U = gates.X(target=control) + gates.Rx(target=qubit, control=control, angle=angle)
    else:
        U = gates.Rx(target=qubit, angle=angle)
    O = ExpectationValue(U=U, H=H)
    E = simulate(O, variables=variables, backend=simulator)
    dO = grad(objective=O, variable='angle')
    dE = simulate(dO,variables=variables)
    assert (numpy.isclose(E, -numpy.sin(angle(variables)), atol=1.e-4))
    assert (numpy.isclose(dE, -numpy.cos(angle(variables)), atol=1.e-4))
    if not silent:
        print("E         =", E)
        print("-sin(angle)=", -numpy.sin(angle(variables)))
        print("dE        =", dE)
        print("-cos(angle)=", -numpy.cos(angle(variables)))


@pytest.mark.parametrize("simulator", [simulators.pick_backend("random"), simulators.pick_backend()])
@pytest.mark.parametrize("controlled", [False, True])
@pytest.mark.parametrize("angle_value", numpy.random.uniform(0.0, 2.0*numpy.pi, 1))
def test_gradient_UHZH_HY(simulator, angle_value, controlled, silent=False):

    angle = Variable(name="angle")
    variables = {angle: angle_value}

    qubit = 0
    H = paulis.Y(qubit=qubit)
    if controlled:
        control = 1
        U = gates.X(target=control) + gates.H(target=qubit)+ gates.Rz(target=qubit, control=control, angle=angle) + gates.H(target=qubit)
    else:
        U = gates.H(target=qubit)+ gates.Rz(target=qubit, angle=angle) + gates.H(target=qubit)
    O = ExpectationValue(U=U, H=H)
    E = simulate(O, variables=variables, backend=simulator)
    dO = grad(objective=O, variable='angle')
    dE = simulate(dO,variables=variables)
    assert (numpy.isclose(E, -numpy.sin(angle(variables)), atol=1.e-4))
    assert (numpy.isclose(dE, -numpy.cos(angle(variables)), atol=1.e-4))
    if not silent:
        print("E         =", E)
        print("-sin(angle)=", -numpy.sin(angle(variables)))
        print("dE        =", dE)
        print("-cos(angle)=", -numpy.cos(angle(variables)))


@pytest.mark.parametrize("simulator", [simulators.pick_backend("random"), simulators.pick_backend()])
@pytest.mark.parametrize("controlled", [False, True])
@pytest.mark.parametrize("angle_value", numpy.random.uniform(0.0, 2.0*numpy.pi, 1))
def test_gradient_UY_HX_wfnsim(simulator, angle_value, controlled, silent=True):
    # same as before just with wavefunction simulation

    # case X Y
    # U = cos(angle/2) + sin(-angle/2)*i*Y
    # <0|Ud H U |0> = cos^2(angle/2)*<0|X|0>
    # + sin^2(-angle/2) <0|YXY|0>
    # + cos(angle/2)*sin(angle/2)*i<0|XY|0>
    # + sin(-angle/2)*cos(angle/2)*(-i) <0|YX|0>
    # = cos^2*0 + sin^2*0 + cos*sin*i(<0|[XY,YX]|0>)
    # = 0.5*sin(-angle)*i <0|[XY,YX]|0> = -0.5*sin(angle)*i * 2 i <0|Z|0>
    # = sin(angle)

    angle = Variable(name="angle")
    variables = {angle: angle_value}

    qubit = 0
    H = paulis.X(qubit=qubit)
    if controlled:
        control = 1
        U = gates.X(target=control) + gates.Ry(target=qubit, control=control, angle=angle)
    else:
        U = gates.Ry(target=qubit, angle=angle)
    O = ExpectationValue(U=U, H=H)
    E = simulate(O, variables=variables, backend=simulator)
    dO = grad(objective=O, variable='angle')
    dE = simulate(dO, variables=variables, backend=simulator)
    E = numpy.float(E)  # for isclose
    dE = numpy.float(dE)  # for isclose
    assert (numpy.isclose(E, numpy.sin(angle(variables)), atol=0.0001))
    assert (numpy.isclose(dE, numpy.cos(angle(variables)), atol=0.0001))
    if not silent:
        print("E         =", E)
        print("sin(angle)=", numpy.sin(angle(variables)))
        print("dE        =", dE)
        print("cos(angle)=", numpy.cos(angle(variables)))


@pytest.mark.parametrize("simulator", [simulators.pick_backend("random"), simulators.pick_backend()])
@pytest.mark.parametrize("controlled", [False, True])
@pytest.mark.parametrize("angle", numpy.random.uniform(0.0, 2.0*numpy.pi, 1))
def test_gradient_UX_HY_wfnsim(simulator, angle, controlled, silent=True):
    # same as before just with wavefunction simulation

    # case YX
    # U = cos(angle/2) + sin(-angle/2)*i*X
    # O = cos*sin*i*<0|YX|0> + sin*cos*(-i)<0|XY|0>
    #   = 0.5*sin(-angle)*i <0|[YX,XY]|0>
    #   = -sin(angle)

    angle_value = angle
    angle = Variable(name="angle")
    variables = {angle: angle_value}

    qubit = 0
    H = paulis.Y(qubit=qubit)
    if controlled:
        control = 1
        U = gates.X(target=control) + gates.Rx(target=qubit, control=control, angle=angle)
    else:
        U = gates.Rx(target=qubit, angle=angle)
    O = ExpectationValue(U=U, H=H)
    E = simulate(O, variables=variables, backend=simulator)
    dO = grad(objective=O, variable=angle)
    dE = simulate(dO,variables=variables)
    assert (numpy.isclose(E, -numpy.sin(angle(variables)), atol=0.0001))
    assert (numpy.isclose(dE, -numpy.cos(angle(variables)), atol=0.0001))
    if not silent:
        print("E         =", E)
        print("-sin(angle)=", -numpy.sin(angle(variables)))
        print("dE        =", dE)
        print("-cos(angle)=", -numpy.cos(angle(variables)))


@pytest.mark.parametrize("simulator", [simulators.pick_backend("random"), simulators.pick_backend()])
@pytest.mark.parametrize("power", numpy.random.uniform(0.0, 2.0, 1))
@pytest.mark.parametrize("controlled", [False, True])
def test_gradient_X(simulator, power,controlled):
    qubit = 0
    control =1
    angle = Variable(name="angle")
    if controlled:
        U =gates.X(target=control) + gates.X(target=qubit, power=angle,control=control)
    else:
        U = gates.X(target=qubit, power=angle)
    angle = Variable(name="angle")
    variables = {angle: power}
    H = paulis.Y(qubit=qubit)
    O = ExpectationValue(U=U, H=H)
    E = simulate(O, variables=variables, backend=simulator)
    dO = grad(objective=O, variable=angle)
    dE = simulate(dO, variables=variables, backend=simulator)
    assert (numpy.isclose(E, -numpy.sin(angle(variables) * (numpy.pi)), atol=1.e-4))
    assert (numpy.isclose(dE, -numpy.pi*numpy.cos(angle(variables) * (numpy.pi)), atol=1.e-4))

@pytest.mark.parametrize("simulator", [simulators.pick_backend("random"), simulators.pick_backend()])
@pytest.mark.parametrize("power", numpy.random.uniform(0.0, 2.0, 1))
@pytest.mark.parametrize("controls",[2,3,4])
def test_gradient_deep_controlled_X(simulator, power,controls):
    qubit = 0
    control = [i for i in range(1,controls+1)]
    angle = Variable(name="angle")
    U =gates.X(target=control) + gates.X(target=qubit, power=angle,control=control)
    angle = Variable(name="angle")
    variables = {angle: power}
    H = paulis.Y(qubit=qubit)
    O = ExpectationValue(U=U, H=H)
    E = simulate(O, variables=variables, backend=simulator)
    dO = grad(objective=O, variable=angle)
    dE = simulate(dO, variables=variables, backend=simulator)
    assert (numpy.isclose(E, -numpy.sin(angle(variables) * (numpy.pi)), atol=1.e-4))
    assert (numpy.isclose(dE, -numpy.pi*numpy.cos(angle(variables) * (numpy.pi)), atol=1.e-4))


@pytest.mark.parametrize("simulator", [simulators.pick_backend("random"), simulators.pick_backend()])
@pytest.mark.parametrize("power", numpy.random.uniform(0.0, 2.0*numpy.pi, 1))
@pytest.mark.parametrize("controlled", [False, True])
def test_gradient_Y(simulator, power,controlled):
    if simulator != "cirq":
        return
    qubit = 0
    control =1
    angle = Variable(name="angle")
    if controlled:
        U =gates.X(target=control) + gates.Y(target=qubit, power=angle,control=control)
    else:
        U = gates.Y(target=qubit, power=angle)
    angle = Variable(name="angle")
    variables = {angle: power}
    H = paulis.X(qubit=qubit)
    O = ExpectationValue(U=U, H=H)
    E = simulate(O, variables=variables, backend=simulator)
    dO = grad(objective=O, variable=angle)
    dE = simulate(dO, variables=variables, backend=simulator)
    assert (numpy.isclose(E, numpy.sin(angle(variables) * (numpy.pi)), atol=1.e-4))
    assert (numpy.isclose(dE, numpy.pi*numpy.cos(angle(variables) * (numpy.pi)), atol=1.e-4))

@pytest.mark.parametrize("simulator", [simulators.pick_backend("random"), simulators.pick_backend()])
@pytest.mark.parametrize("power", numpy.random.uniform(0.0, 2.0, 1))
@pytest.mark.parametrize("controls",[2,3,4])
def test_gradient_deep_controlled_Y(simulator, power,controls):
    qubit = 0
    control = [i for i in range(1,controls+1)]
    angle = Variable(name="angle")
    U =gates.X(target=control) + gates.Y(target=qubit, power=angle,control=control)
    angle = Variable(name="angle")
    variables = {angle: power}
    H = paulis.X(qubit=qubit)
    O = ExpectationValue(U=U, H=H)
    E = simulate(O, variables=variables, backend=simulator)
    dO = grad(objective=O, variable=angle)
    dE = simulate(dO, variables=variables, backend=simulator)
    assert (numpy.isclose(E, numpy.sin(angle(variables) * (numpy.pi)), atol=1.e-4))
    assert (numpy.isclose(dE, numpy.pi*numpy.cos(angle(variables) * (numpy.pi)), atol=1.e-4))


@pytest.mark.parametrize("simulator", [simulators.pick_backend("random"), simulators.pick_backend()])
@pytest.mark.parametrize("power", numpy.random.uniform(0.0, 2.0, 1))
@pytest.mark.parametrize("controlled", [False, True])
def test_gradient_Z(simulator, power,controlled):
    qubit = 0
    control =1
    angle = Variable(name="angle")
    if controlled:
        U =gates.X(target=control) + gates.H(target=qubit) + gates.Z(target=qubit, power=angle,control=control) + gates.H(target=qubit)
    else:
        U = gates.H(target=qubit) + gates.Z(target=qubit, power=angle) + gates.H(target=qubit)
    angle = Variable(name="angle")
    variables = {angle: power}
    H = paulis.Y(qubit=qubit)
    O = ExpectationValue(U=U, H=H)
    E = simulate(O, variables=variables, backend=simulator)
    dO = grad(objective=O, variable=angle)
    dE = simulate(dO, variables=variables, backend=simulator)
    assert (numpy.isclose(E, -numpy.sin(angle(variables) * (numpy.pi)), atol=1.e-4))
    assert (numpy.isclose(dE, -numpy.pi*numpy.cos(angle(variables) * (numpy.pi)), atol=1.e-4))

@pytest.mark.parametrize("simulator", [simulators.pick_backend("random"), simulators.pick_backend()])
@pytest.mark.parametrize("power", numpy.random.uniform(0.0, 2.0, 1))
@pytest.mark.parametrize("controls",[2,3,4])
def test_gradient_deep_controlled_Z(simulator, power,controls):
    qubit = 0
    control = [i for i in range(1,controls+1)]
    angle = Variable(name="angle")
    U =gates.X(target=control) + gates.H(target=qubit) + gates.Z(target=qubit, power=angle,control=control) + gates.H(target=qubit)
    angle = Variable(name="angle")
    variables = {angle: power}
    H = paulis.Y(qubit=qubit)
    O = ExpectationValue(U=U, H=H)
    E = simulate(O, variables=variables, backend=simulator)
    dO = grad(objective=O, variable=angle)
    dE = simulate(dO, variables=variables, backend=simulator)
    assert (numpy.isclose(E, -numpy.sin(angle(variables) * (numpy.pi)), atol=1.e-4))
    assert (numpy.isclose(dE, -numpy.pi*numpy.cos(angle(variables) * (numpy.pi)), atol=1.e-4))


@pytest.mark.parametrize("simulator", [simulators.pick_backend("random"), simulators.pick_backend()])
@pytest.mark.parametrize("power", numpy.random.uniform(0.0, 2.0*numpy.pi, 1))
@pytest.mark.parametrize("controlled", [False, True])
def test_gradient_H(simulator, power,controlled):
    qubit = 0
    control =1
    angle = Variable(name="angle")
    variables = {angle:power}

    H = paulis.X(qubit=qubit)
    if not controlled:
        U = gates.H(target=qubit, power=angle)
    else:
        U= gates.X(target=control) + gates.H(target=qubit,control=control, power=angle)

    O = ExpectationValue(U=U, H=H)
    E = simulate(O, variables=variables, backend=simulator)
    assert (numpy.isclose(E, -numpy.cos(angle(variables) * (numpy.pi))/2 +0.5, atol=1.e-4))
    dO = grad(objective=O, variable=angle)
    dE = simulate(dO, variables=variables, backend=simulator)

    assert (numpy.isclose(dE, numpy.pi*numpy.sin(angle(variables) * (numpy.pi))/2, atol=1.e-4))

@pytest.mark.parametrize("simulator", [simulators.pick_backend()])
@pytest.mark.parametrize("power", numpy.random.uniform(0.0, 2.0*numpy.pi, 1))
@pytest.mark.parametrize("controls", [3])
def test_gradient_deep_H(simulator, power,controls):
    qubit = 0
    angle = Variable(name="angle")
    variables = {angle:power}
    control = [i for i in range(1, controls + 1)]
    H = paulis.X(qubit=qubit)

    U= gates.X(target=control) + gates.H(target=qubit,control=control, power=angle)

    O = ExpectationValue(U=U, H=H)
    E = simulate(O, variables=variables, backend=simulator)
    assert (numpy.isclose(E, -numpy.cos(angle(variables) * (numpy.pi))/2 +0.5, atol=1.e-4))
    dO = grad(objective=O, variable=angle)
    dE = simulate(dO, variables=variables, backend=simulator)

    assert (numpy.isclose(dE, numpy.pi*numpy.sin(angle(variables) * (numpy.pi))/2, atol=1.e-4))