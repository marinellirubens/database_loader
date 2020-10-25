"""Module to test database_loader.core.loader.py methods"""
from __future__ import (absolute_import, division, print_function)

import sys
import os
import pytest
import builtins
from unittest import mock

dir_path = os.path.dirname(os.path.realpath(__file__))
parent_dir_path = os.path.abspath(os.path.join(dir_path, os.pardir))
sys.path.insert(0, parent_dir_path)

from database_loader.core import loader


def test_print_version(mocker):
    """Test print_version method"""
    exit_call = mocker.patch.object(builtins, 'exit')
    loader.print_version()
    exit_call.assert_called_with(0)


@pytest.mark.parametrize(
    argnames="params, arguments, values",
    argvalues=[
        (["-c", '100', "-t", "tb_users"],
         ['commit', 'table', 'verbose', 'clean', 'connection_type',
          'database_type', 'type', 'version'],
         [100, 'tb_users', False, False, 'TNS', 'ORACLE', 'TSV', False]),
        (['-c', '100', '-t', 'tb_users', '-u', 'root', '-d', 'TESTEDB', '-p',
          '123456', '-f', 'teste.tsv'],
         ['commit', 'table', 'verbose', 'clean', 'connection_type',
          'database_type', 'type', 'version', 'user', 'database',
          'password', 'file_load'],
         [100, 'tb_users', False, False, 'TNS', 'ORACLE', 'TSV', False, 'root',
          'TESTEDB', '123456', 'teste.tsv'])],
    ids=['basic_version', 'string_connection']
)
def test_get_arguments(mocker, params, arguments, values):
    parameters = loader.get_arguments(params)
    for argument, value in zip(arguments, values):
        param = eval(f'parameters.{argument}')
        assert param == value
