# Copyright 2021 Q-CTRL
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Tests conversion to Qiskit Circuit
"""

import numpy as np
from qctrlopencontrols import (new_carr_purcell_sequence, new_cpmg_sequence,
                               new_periodic_sequence, new_quadratic_sequence,
                               new_spin_echo_sequence, new_uhrig_sequence,
                               new_walsh_sequence, new_x_concatenated_sequence,
                               new_xy_concatenated_sequence)
from qctrlqiskit import convert_dds_to_qiskit_quantum_circuit
from qiskit import BasicAer, execute

_callable = {
    "Spin echo": new_spin_echo_sequence,
    "Carr-Purcell": new_carr_purcell_sequence,
    "Carr-Purcell-Meiboom-Gill": new_cpmg_sequence,
    "Uhrig single-axis": new_uhrig_sequence,
    "periodic single-axis": new_periodic_sequence,
    "quadratic": new_quadratic_sequence,
    "Walsh single-axis": new_walsh_sequence,
    "Quadratic": new_quadratic_sequence,
    "X concatenated": new_x_concatenated_sequence,
    "XY concatenated": new_xy_concatenated_sequence,
}


def _create_test_sequence(sequence_scheme, pre_post_rotation):

    """
    Create a DD sequence of choice.

    Parameters
    ----------
    sequence_scheme : str
        One of 'Spin echo', 'Carr-Purcell', 'Carr-Purcell-Meiboom-Gill',
        'Uhrig single-axis', 'Periodic single-axis', 'Walsh single-axis',
        'Quadratic', 'X concatenated',
        'XY concatenated'
    pre_post_rotation : bool
        If True, adds a :math:`X_{\\pi/2}` gate on either ends

    Returns
    -------
    DynamicDecouplingSequence
        The Dynamical Decoupling Sequence instance built from supplied
        schema information
    """

    dd_sequence_params = {}
    dd_sequence_params["duration"] = 4
    dd_sequence_params["pre_post_rotation"] = pre_post_rotation

    # 'spin_echo' does not need any additional parameter

    if sequence_scheme in [
        "Carr-Purcell",
        "Carr-Purcell-Meiboom-Gill",
        "Uhrig single-axis",
        "periodic single-axis",
    ]:

        dd_sequence_params["offset_count"] = 2

    elif sequence_scheme in ["Walsh single-axis"]:

        dd_sequence_params["paley_order"] = 5

    elif sequence_scheme in ["quadratic"]:

        dd_sequence_params["duration"] = 16
        dd_sequence_params["outer_offset_count"] = 4
        dd_sequence_params["inner_offset_count"] = 4

    elif sequence_scheme in ["X concatenated", "XY concatenated"]:

        dd_sequence_params["duration"] = 16
        dd_sequence_params["concatenation_order"] = 2

    sequence = _callable[sequence_scheme](**dd_sequence_params)
    return sequence


def _check_circuit_unitary(pre_post_rotation, algorithm):
    """
    Checks that the unitary of a dynamic decoupling operation is the identity.
    """

    backend = "unitary_simulator"
    number_of_shots = 1
    backend_simulator = BasicAer.get_backend(backend)

    for sequence_scheme in [
        "Carr-Purcell",
        "Carr-Purcell-Meiboom-Gill",
        "Uhrig single-axis",
        "periodic single-axis",
        "Walsh single-axis",
        "quadratic",
        "X concatenated",
        "XY concatenated",
    ]:
        sequence = _create_test_sequence(sequence_scheme, pre_post_rotation)
        quantum_circuit = convert_dds_to_qiskit_quantum_circuit(
            dynamic_decoupling_sequence=sequence,
            add_measurement=False,
            algorithm=algorithm,
        )

        job = execute(quantum_circuit, backend_simulator, shots=number_of_shots)
        result = job.result()
        unitary = result.get_unitary(quantum_circuit)

        assert np.isclose(np.abs(np.trace(unitary)), 2.0)


def test_identity_operation():

    """Tests if the Dynamic Decoupling Sequence gives rise to Identity
    operation in Qiskit
    """
    _check_circuit_unitary(False, "instant unitary")

    _check_circuit_unitary(True, "instant unitary")

    _check_circuit_unitary(False, "fixed duration unitary")

    _check_circuit_unitary(True, "fixed duration unitary")


if __name__ == "__main__":
    pass
