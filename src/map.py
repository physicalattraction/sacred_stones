import json
import os.path
from typing import List, Dict, TypedDict, Tuple

import constants


class MonsterAssignment(TypedDict):
    name: str
    kind: str


class CellDefinition(TypedDict, total=False):
    tile: str
    player: bool
    monster: MonsterAssignment


WorldMap = List[str]  # Textual representation of the map
MapLegend = Dict[str, CellDefinition]  # Mapping from each character in the map to its info


def read_map(zone_identifier: str) -> Tuple[WorldMap, MapLegend]:
    """
    Read the map.txt and map_legend.json files for the current zone
    """

    # TODO: Prevent reading the files twice

    map_legend_file = os.path.join(constants.DATA_DIR, 'zones', zone_identifier, constants.MAP_LEGEND_FILE)
    with open(map_legend_file, 'r') as f:
        map_legend = json.load(f)
    map_file = os.path.join(constants.DATA_DIR, 'zones', zone_identifier, constants.MAP_FILE)
    with open(map_file, 'r') as f:
        world_map = [i.strip() for i in f.readlines()]
    return world_map, map_legend
