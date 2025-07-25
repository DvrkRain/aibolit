# SPDX-FileCopyrightText: Copyright (c) 2019-2025 Aibolit
# SPDX-License-Identifier: MIT

"""Configuration module for aibolit.

This module defines configuration factories and providers for patterns and metrics,
providing a central registry for all available code analysis tools.
"""
import os
import typing
from pathlib import Path

from aibolit.ast_framework import ASTNodeType

from aibolit.ast_framework.ast import AST
from aibolit.metrics.number_variables.numVariables import NumVars as M7
from aibolit.metrics.cognitiveC.cognitive_c import CognitiveComplexity as M4
from aibolit.metrics.entropy.entropy import Entropy as M1
from aibolit.metrics.lcom4.lcom4 import LCOM4 as M5
from aibolit.metrics.max_diameter.max_diameter import MaxDiameter as M6
from aibolit.metrics.ncss.ncss import NCSSMetric as M2
from aibolit.metrics.spaces.SpaceCounter import IndentationCounter as M3
from aibolit.metrics.NumberMethods.NumberMethods import NumberMethods as M8
from aibolit.metrics.RFC.rfc import RFC as M9
from aibolit.metrics.fanout.FanOut import FanOut as M10
from aibolit.metrics.cc.main import CCMetric as M11
from aibolit.patterns.array_as_argument.array_as_argument import ArrayAsArgument as P22
from aibolit.patterns.assert_in_code.assert_in_code import AssertInCode as P1
from aibolit.patterns.assign_null_finder.assign_null_finder import NullAssignment as P28
from aibolit.patterns.classic_setter.classic_setter import ClassicSetter as P2
from aibolit.patterns.empty_rethrow.empty_rethrow import EmptyRethrow as P3
from aibolit.patterns.er_class.er_class import ErClass as P4
from aibolit.patterns.force_type_casting_finder.force_type_casting_finder import \
    ForceTypeCastingFinder as P5
from aibolit.patterns.if_return_if_detection.if_detection import CountIfReturn as P6
from aibolit.patterns.implements_multi.implements_multi import ImplementsMultiFinder as P7
from aibolit.patterns.incomplete_for.incomplete_for import IncompleteFor as P33
from aibolit.patterns.instanceof.instance_of import InstanceOf as P8
from aibolit.patterns.joined_validation.joined_validation import JoinedValidation as P23
from aibolit.patterns.many_primary_ctors.many_primary_ctors import ManyPrimaryCtors as P9
from aibolit.patterns.method_chaining.method_chaining import MethodChainFind as P10
from aibolit.patterns.multiple_try.multiple_try import MultipleTry as P11
from aibolit.patterns.multiple_while.multiple_while import MultipleWhile as P29
from aibolit.patterns.nested_blocks.nested_blocks import NestedBlocks as P32
from aibolit.patterns.non_final_attribute.non_final_attribute import NonFinalAttribute as P12
from aibolit.patterns.non_final_class.non_final_class import NonFinalClass as P24
from aibolit.patterns.null_check.null_check import NullCheck as P13
from aibolit.patterns.partially_synchronized_methods.partially_synchronized_methods import (
    PartiallySynchronizedMethods as P14
)
from aibolit.patterns.private_static_method.private_static_method import PrivateStaticMethod as P25
from aibolit.patterns.protected_method.protected_method import ProtectedMethod as P30
from aibolit.patterns.public_static_method.public_static_method import PublicStaticMethod as P26
from aibolit.patterns.redundant_catch.redundant_catch import RedundantCatch as P15
from aibolit.patterns.return_null.return_null import ReturnNull as P16
from aibolit.patterns.send_null.send_null import SendNull as P31
from aibolit.patterns.string_concat.string_concat import StringConcatFinder as P17
from aibolit.patterns.supermethod.supermethod import SuperMethod as P18
from aibolit.patterns.hybrid_constructor.hybrid_constructor import HybridConstructor as P19
from aibolit.patterns.var_decl_diff.var_decl_diff import VarDeclarationDistance as P20
from aibolit.patterns.var_middle.var_middle import VarMiddle as P21
from aibolit.patterns.var_siblings.var_siblings import VarSiblings as P27
from aibolit.types_decl import LineNumber


class Singleton(type):
    """Metaclass for implementing the Singleton pattern."""
    _instances = {}  # type: ignore

    def __call__(cls, *args, **kwargs):
        """Create or return the singleton instance."""
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


@typing.runtime_checkable
class Pattern(typing.Protocol):
    def value(self, ast: AST) -> list[LineNumber]:
        ...


class PatternsConfigEntry(typing.TypedDict):
    name: str
    code: str
    make: typing.Callable[[], Pattern]


@typing.runtime_checkable
class Metric(typing.Protocol):
    def value(self, ast: AST) -> int:
        ...


class MetricsConfigEntry(typing.TypedDict):
    name: str
    code: str
    make: typing.Callable[[], Metric]


class PatternsConfig(typing.TypedDict):
    patterns: list[PatternsConfigEntry]
    metrics: list[MetricsConfigEntry]
    patterns_exclude: list[str]
    metrics_exclude: list[str]
    target: dict


class Config(metaclass=Singleton):
    """Central configuration for patterns and metrics discovery."""

    @staticmethod
    def home_aibolit_folder():
        """Get the home folder for aibolit."""
        return os.environ.get('HOME_AIBOLIT') or '/home/jovyan/aibolit'

    @staticmethod
    def folder_to_save_model_data():
        """Get the folder path for saving model data."""
        model_folder = Path(Config().home_aibolit_folder(), 'aibolit', 'binary_files')
        return os.environ.get('SAVE_MODEL_FOLDER') or model_folder

    @staticmethod
    def folder_model_data():
        """Get the folder path for model data."""
        dir_path = os.path.dirname(os.path.realpath(__file__))
        model_file = Path(Path(dir_path), 'binary_files', 'model.pkl')
        return os.environ.get('HOME_MODEL_FOLDER') or model_file

    @staticmethod
    def dataset_file():
        """Get the dataset file path."""
        dataset_path = Path(Config().home_aibolit_folder(), 'scripts', 'target', 'dataset.csv')
        return os.environ.get('HOME_DATASET_CSV') or dataset_path

    @staticmethod
    def train_csv():
        """Get the training CSV file path."""
        return os.environ.get('HOME_TRAIN_DATASET')

    @staticmethod
    def test_csv():
        """Get the test CSV file path."""
        return os.environ.get('HOME_TEST_DATASET')

    @staticmethod
    def get_patterns_config() -> PatternsConfig:
        """Get the patterns configuration dictionary."""
        return {  # ty: ignore[invalid-return-type] until https://github.com/astral-sh/ty/issues/154
            'patterns': [
                {'name': 'Asserts', 'code': 'P1', 'make': P1},
                {'name': 'Setters', 'code': 'P2', 'make': P2},
                {'name': 'Empty Rethrow', 'code': 'P3', 'make': P3},
                {'name': 'Prohibited class name', 'code': 'P4', 'make': P4},
                {'name': 'Force Type Casting', 'code': 'P5', 'make': P5},
                {'name': 'Count If Return', 'code': 'P6', 'make': P6},
                {'name': 'Implements Multi', 'code': 'P7', 'make': P7},
                {'name': 'Instance of', 'code': 'P8', 'make': P8},
                {'name': 'Many primary constructors', 'code': 'P9', 'make': P9},
                {'name': 'Method chain', 'code': 'P10', 'make': P10},
                {'name': 'Multiple try', 'code': 'P11', 'make': P11},
                {'name': 'Non final attribute', 'code': 'P12', 'make': P12},
                {'name': 'Null check', 'code': 'P13', 'make': P13},
                {'name': 'Partial synchronized', 'code': 'P14', 'make': P14},
                {'name': 'Redundant catch', 'code': 'P15', 'make': P15},
                {'name': 'Return null', 'code': 'P16', 'make': P16},
                {'name': 'String concat', 'code': 'P17', 'make': P17},
                {'name': 'Super Method', 'code': 'P18', 'make': P18},
                {'name': 'This in constructor', 'code': 'P19', 'make': P19},
                {
                    'name': 'Var declaration distance for 5 lines',
                    'code': 'P20_5',
                    'make': lambda: P20(5)
                },
                {
                    'name': 'Var declaration distance for 7 lines',
                    'code': 'P20_7',
                    'make': lambda: P20(7)
                },
                {
                    'name': 'Var declaration distance for 11 lines',
                    'code': 'P20_11',
                    'make': lambda: P20(11)
                },
                {'name': 'Var in the middle', 'code': 'P21', 'make': P21},
                {'name': 'Array as function argument', 'code': 'P22', 'make': P22},
                {'name': 'Joined validation', 'code': 'P23', 'make': P23},
                {'name': 'Non final class', 'code': 'P24', 'make': P24},
                {'name': 'Private static method', 'code': 'P25', 'make': P25},
                {'name': 'Public static method', 'code': 'P26', 'make': P26},
                {'name': 'Var siblings', 'code': 'P27', 'make': P27},
                {'name': 'Null Assignment', 'code': 'P28', 'make': P28},
                {'name': 'Multiple While', 'code': 'P29', 'make': P29},
                {'name': 'Protected Method', 'code': 'P30', 'make': P30},
                {'name': 'Send Null', 'code': 'P31', 'make': P31},
                {'name': 'Nested Loop', 'code': 'P32',
                 'make': lambda: P32(2, ASTNodeType.DO_STATEMENT,
                                     ASTNodeType.FOR_STATEMENT,
                                     ASTNodeType.WHILE_STATEMENT)},
                {'name': 'Incomplete For', 'code': 'P33', 'make': P33},
            ],
            'metrics': [
                {'name': 'Entropy', 'code': 'M1', 'make': M1},  # type: ignore
                {'name': 'NCSS lightweight', 'code': 'M2', 'make': M2},
                {
                    'name': 'Indentation counter: Right total variance',
                    'code': 'M3_1',
                    'make': lambda: M3(right_var=True)  # type: ignore
                },
                {
                    'name': 'Indentation counter: Left total variance',
                    'code': 'M3_2',
                    'make': lambda: M3(left_var=True)  # type: ignore
                },
                {
                    'name': 'Indentation counter: Right max variance',
                    'code': 'M3_3',
                    'make': lambda: M3(max_right=True)  # type: ignore
                },
                {
                    'name': 'Indentation counter: Left max variance',
                    'code': 'M3_4',
                    'make': lambda: M3(max_left=True)  # type: ignore
                },
                {'name': 'Cognitive Complexity', 'code': 'M4', 'make': M4},
                {'name': 'LCOM4', 'code': 'M5', 'make': M5},  # type: ignore
                {'name': 'Max diameter of AST', 'code': 'M6', 'make': M6},
                {'name': 'Number of variables', 'code': 'M7', 'make': M7},  # type: ignore
                {'name': 'Number of methods', 'code': 'M8', 'make': M8},
                {'name': 'Responce for class', 'code': 'M9', 'make': M9},
                {'name': 'Fan out', 'code': 'M10', 'make': M10},
                {'name': 'Cyclomatic Complexity', 'code': 'M11', 'make': M11},
            ],
            'target': {

            },
            'patterns_exclude': [
                'P9',  # patterns based on text cannot accept arbitrary AST
            ],
            'metrics_exclude': ['M1', 'M3_1', 'M3_2', 'M3_3', 'M3_4', 'M5', 'M7', 'M8']
        }
