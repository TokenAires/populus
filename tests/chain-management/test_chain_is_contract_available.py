import pytest

from populus.utils.linking import (
    link_bytecode_by_name,
)
from populus import Project


def test_contract_availability_with_no_dependencies(temp_chain, math, register_address):
    chain = temp_chain

    register_address('Math', math.address)

    is_available = chain.is_contract_available('Math')
    assert is_available is True


def test_contract_availability_when_not_registered(temp_chain):
    chain = temp_chain

    is_available = chain.is_contract_available('Math')
    assert is_available is False


def test_contract_availability_with_missing_dependency(temp_chain,
                                                       multiply_13,
                                                       register_address):
    chain = temp_chain

    register_address('Multiply13', multiply_13.address)

    is_available = chain.is_contract_available('Multiply13')
    assert is_available is False


def test_contract_availability_with_bytecode_mismatch(temp_chain,
                                                      library_13,
                                                      math,
                                                      register_address):
    chain = temp_chain

    register_address('Math', library_13.address)

    is_available = chain.is_contract_available('Math')
    assert is_available is False


def test_contract_availability_skipping_bytecode_validation(temp_chain,
                                                            library_13,
                                                            math,
                                                            register_address):
    chain = temp_chain

    register_address('Math', library_13.address)

    is_available = chain.is_contract_available('Math', validate_bytecode=False)
    assert is_available is True


def test_contract_availability_with_bytecode_mismatch_on_dependency(temp_chain,
                                                                    multiply_13,
                                                                    math,
                                                                    register_address):
    chain = temp_chain

    register_address('Multiply13', multiply_13.address)
    register_address('Library13', math.address)

    is_available = chain.is_contract_available('Multiply13')
    assert is_available is False


def test_contract_availability_with_dependency(temp_chain,
                                               multiply_13,
                                               library_13,
                                               register_address):
    chain = temp_chain

    register_address('Multiply13', multiply_13.address)
    register_address('Library13', library_13.address)

    is_available = chain.is_contract_available('Multiply13')
    assert is_available is True


def test_contract_availability_with_declared_dependency(temp_chain,
                                                        multiply_13,
                                                        library_13,
                                                        register_address):
    chain = temp_chain

    register_address('Multiply13', multiply_13.address)

    is_available = chain.is_contract_available(
        'Multiply13',
        link_dependencies={'Library13': library_13.address},
    )
    assert is_available is True
