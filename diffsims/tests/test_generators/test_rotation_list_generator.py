# -*- coding: utf-8 -*-
# Copyright 2017-2020 The diffsims developers
#
# This file is part of diffsims.
#
# diffsims is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# diffsims is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with diffsims.  If not, see <http://www.gnu.org/licenses/>.

import pytest
import numpy as np
from diffsims.generators.rotation_list_generators import (
    get_local_grid,
    get_grid_around_beam_direction,
    get_fundamental_zone_grid,
    get_beam_directions_grid,
)
from diffsims.generators.sphere_mesh_generators import _get_max_grid_angle


@pytest.mark.parametrize(
    "grid",
    [
        pytest.param(get_local_grid(resolution=30, center=(0, 1, 0), grid_width=35)),
        get_fundamental_zone_grid(space_group=20, resolution=20),
    ],
)
def test_get_grid(grid):
    assert isinstance(grid, list)
    assert len(grid) > 0
    assert isinstance(grid[0], tuple)


def test_get_grid_around_beam_direction():
    grid = get_grid_around_beam_direction(
        (0, 90, 0), resolution=2, angular_range=(0, 9)
    )
    assert isinstance(grid, list)
    assert isinstance(grid[0], tuple)
    assert len(grid) == 5  # should have 0,2,4,6 and 8
    assert np.allclose([x[1] for x in grid], 90)  # taking z to y


@pytest.mark.parametrize(
    "mesh",
    [
        "uv_sphere",
        "normalized_cube",
        "spherified_cube_edge",
        "spherified_cube_corner",
        "icosahedral",
    ],
)
@pytest.mark.parametrize(
    "crystal_system",
    [
        "cubic",
        "hexagonal",
        "trigonal",
        "tetragonal",
        "orthorhombic",
        "monoclinic",
        "triclinic",
    ],
)
def test_get_beam_directions_grid(crystal_system, mesh):
    grid = get_beam_directions_grid(crystal_system, 5, mesh=mesh)
    # convert grid back to xyz
    max_angle = _get_max_grid_angle(grid)
    assert max_angle <= 5

@pytest.mark.xfail()
def test_invalid_mesh_beam_directions():
    _ = get_beam_directions_grid("cubic", 10, mesh="invalid")
