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
qiskit.quantum_circuit
"""

import numpy as np
from qctrlopencontrols import DynamicDecouplingSequence
from qctrlopencontrols.exceptions import ArgumentsValueError
from qiskit import (
    ClassicalRegister,
    QuantumCircuit,
    QuantumRegister,
)
from qiskit.qasm import pi

FIX_DURATION_UNITARY = "fixed duration unitary"
INSTANT_UNITARY = "instant unitary"


def convert_dds_to_qiskit_quantum_circuit(
    dynamic_decoupling_sequence,
    target_qubits=None,
    gate_time=0.1,
    add_measurement=True,
    algorithm=INSTANT_UNITARY,
    quantum_registers=None,
    circuit_name=None,
):
    """Converts a Dynamic Decoupling Sequence into QuantumCircuit
    as defined in Qiskit

    Parameters
    ----------
    dynamic_decoupling_sequence : DynamicDecouplingSequence
        The dynamic decoupling sequence
    target_qubits : list, optional
        List of integers specifying target qubits for the sequence operation;
        defaults to None
    gate_time : float, optional
        Time (in seconds) delay introduced by a gate; defaults to 0.1
    add_measurement : bool, optional
        If True, the circuit contains a measurement operation for each of the
        target qubits and a set of ClassicalRegister objects created with length
        equal to `len(target_qubits)`
    algorithm : str, optional
        One of 'fixed duration unitary' or 'instant unitary'; In the case of
        'fixed duration unitary', the sequence operations are assumed to be
        taking the amount of gate_time while 'instant unitary' assumes the sequence
        operations are instantaneous (and hence does not contribute to the delay between
        offsets). Defaults to 'instant unitary'.
    quantum_registers : QuantumRegister, optional
        The set of quantum registers; defaults to None
        If not None, it must have the target qubit specified in `target_qubit`
        indices list
    circuit_name : str, optional
        A string indicating the name of the circuit; defaults to None

    Returns
    -------
    QuantumCircuit
        The circuit defined from the specified dynamic decoupling sequence

    Raises
    ------
    ArgumentsValueError
        If any of the input parameters are invalid

    Notes
    -----

    Dynamic Decoupling Sequences (DDS) consist of idealized pulse operation. Theoretically,
    these operations (pi-pulses in X,Y or Z) occur instantaneously. However, in practice,
    pulses require time. Therefore, this method of converting an idealized sequence
    results to a circuit that is only an approximate implementation of the idealized sequence.

    In idealized definition of DDS, `offsets` represents the instances within sequence
    `duration` where a pulse occurs instantaneously. A series of appropriate circuit component
    is placed in order to represent these pulses. The `gaps` or idle time in between active
    pulses are filled up with `identity` gates. Each identity gate introduces a delay of
    `gate_time`. In this implementation, the number of identity gates is determined by
    :math:`np.int(np.floor(offset\\_distance / gate\\_time))`. As a consequence, the duration of
    the real-circuit is :math:`gate\\_time \\times number\\_of\\_identity\\_gates +
    pulse\\_gate\\_time \\times number\\_of\\_pulses`.

    Q-CTRL Qiskit Adapter supports operation resulting in rotation around at most one axis at
    any offset.
    """

    if dynamic_decoupling_sequence is None:
        raise ArgumentsValueError(
            "No dynamic decoupling sequence provided.",
            {"dynamic_decoupling_sequence": dynamic_decoupling_sequence},
        )

    if not isinstance(dynamic_decoupling_sequence, DynamicDecouplingSequence):
        raise ArgumentsValueError(
            "Dynamical decoupling sequence is not recognized."
            "Expected DynamicDecouplingSequence instance",
            {"type(dynamic_decoupling_sequence)": type(dynamic_decoupling_sequence)},
        )

    target_qubits = target_qubits or [0]

    if gate_time <= 0:
        raise ArgumentsValueError(
            "Time delay of identity gate must be greater than zero.",
            {"gate_time": gate_time},
        )

    if np.any(target_qubits) < 0:
        raise ArgumentsValueError(
            "Every target qubits index must be non-negative.",
            {"target_qubits": target_qubits},
        )

    if algorithm not in [FIX_DURATION_UNITARY, INSTANT_UNITARY]:
        raise ArgumentsValueError(
            f"Algorithm must be one of {INSTANT_UNITARY} or {FIX_DURATION_UNITARY}",
            {"algorithm": algorithm},
        )

    if quantum_registers is not None:
        if (max(target_qubits) + 1) > len(quantum_registers):
            raise ArgumentsValueError(
                "Target qubit is not present in quantum_registers",
                {
                    "target_qubits": target_qubits,
                    "size(quantum_registers)": len(quantum_registers),
                },
                extras={"max(target_qubits)": max(target_qubits)},
            )
    else:
        quantum_registers = QuantumRegister(max(target_qubits) + 1)

    classical_registers = None
    if add_measurement:
        classical_registers = ClassicalRegister(len(target_qubits))
        quantum_circuit = QuantumCircuit(quantum_registers, classical_registers)
    else:
        quantum_circuit = QuantumCircuit(quantum_registers)

    if circuit_name is not None:
        quantum_circuit.name = circuit_name

    unitary_time = 0.0
    if algorithm == FIX_DURATION_UNITARY:
        unitary_time = gate_time

    rabi_rotations = dynamic_decoupling_sequence.rabi_rotations
    azimuthal_angles = dynamic_decoupling_sequence.azimuthal_angles
    detuning_rotations = dynamic_decoupling_sequence.detuning_rotations

    offsets = dynamic_decoupling_sequence.offsets

    time_covered = 0
    for offset, rabi_rotation, azimuthal_angle, detuning_rotation in zip(
        list(offsets),
        list(rabi_rotations),
        list(azimuthal_angles),
        list(detuning_rotations),
    ):

        offset_distance = offset - time_covered

        if np.isclose(offset_distance, 0.0):
            offset_distance = 0.0

        if offset_distance < 0:
            raise ArgumentsValueError(
                "Offsets cannot be placed properly. Spacing between the rotations"
                "is smaller than the time required to perform the rotation. Provide"
                "a longer dynamic decoupling sequence or shorted gate time.",
                {
                    "dynamic_decoupling_sequence": dynamic_decoupling_sequence,
                    "gate_time": gate_time,
                },
            )

        while (time_covered + gate_time) <= offset:
            for qubit in target_qubits:
                quantum_circuit.iden(  # pylint: disable=no-member
                    quantum_registers[qubit]
                )
                quantum_circuit.barrier(  # pylint: disable=no-member
                    quantum_registers[qubit]
                )
            time_covered += gate_time

        x_rotation = rabi_rotation * np.cos(azimuthal_angle)
        y_rotation = rabi_rotation * np.sin(azimuthal_angle)
        z_rotation = detuning_rotation

        rotations = np.array([x_rotation, y_rotation, z_rotation])
        zero_pulses = np.isclose(rotations, 0.0).astype(np.int)
        nonzero_pulse_counts = 3 - np.sum(zero_pulses)
        if nonzero_pulse_counts > 1:
            raise ArgumentsValueError(
                "Open Controls support a sequence with one "
                "valid rotation at any offset. Found a sequence "
                "with multiple rotation operations at an offset.",
                {"dynamic_decoupling_sequence": dynamic_decoupling_sequence},
                extras={
                    "offset": offset,
                    "rabi_rotation": rabi_rotation,
                    "azimuthal_angle": azimuthal_angle,
                    "detuning_rotation": detuning_rotation,
                },
            )

        for qubit in target_qubits:
            if nonzero_pulse_counts == 0:
                quantum_circuit.u3(
                    0.0, 0.0, 0.0, quantum_registers[qubit]  # pylint: disable=no-member
                )
            else:
                if not np.isclose(rotations[0], 0.0):
                    quantum_circuit.u3(
                        rotations[0],
                        -pi / 2,
                        pi / 2,  # pylint: disable=no-member
                        quantum_registers[qubit],
                    )
                elif not np.isclose(rotations[1], 0.0):
                    quantum_circuit.u3(
                        rotations[1],
                        0.0,
                        0.0,  # pylint: disable=no-member
                        quantum_registers[qubit],
                    )
                elif not np.isclose(rotations[2], 0.0):
                    quantum_circuit.u1(
                        rotations[2],  # pylint: disable=no-member
                        quantum_registers[qubit],
                    )
            quantum_circuit.barrier(
                quantum_registers[qubit]
            )  # pylint: disable=no-member

        time_covered = offset + unitary_time

    if add_measurement:
        for q_index, qubit in enumerate(target_qubits):
            quantum_circuit.measure(  # pylint: disable=no-member
                quantum_registers[qubit], classical_registers[q_index]
            )

    return quantum_circuit
