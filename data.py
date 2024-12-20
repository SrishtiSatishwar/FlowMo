# Paths
#paths = {
#    "PATH1": ["RC1-C1", "RC1-C2", "RC1-C3", "RC2-C5"],
#    "PATH2": ["RC1-C1","RC2-C1", "RC2-C2", "RC2-C3", "RC2-C4", "RC2-C5"]
#}

# Camera network represented as an adjacency list
cameraGraph = {
    "RC1C1": ["RC1C2", "RC2C1"],  # RC1-C1 connects to RC1-C2 and RC2-C1
    "RC1C2": ["RC1C1", "RC1C3"],
    "RC1C3": ["RC1C2", "RC2C5"],
    "RC2C1": ["RC1C1", "RC2C2"],
    "RC2C2": ["RC2C1", "RC2C3"],
    "RC2C3": ["RC2C2", "RC2C4"],
    "RC2C4": ["RC2C3", "RC2C5"],
    "RC2C5": ["RC1C3", "RC2C4"],
}

cameraPaths = {
    ("RC1C1", "RC1C2"): [(99, 438), (237, 355)],  # Pathcoordinates between RC1C1 and RC1C2
    ("RC1C1", "RC2C1"): [(199, 522), (99, 438)],
    ("RC1C2", "RC1C3"): [(434, 235), (237, 355)],
    ("RC2C1", "RC2C2"): [(299, 522), (249, 535), (199, 522)],
    ("RC2C2", "RC2C3"): [(424, 404),(318, 505)],
    ("RC2C3", "RC2C4"): [(644, 333), (624, 333), (444, 384), (424, 404)],
    ("RC2C4", "RC2C5"): [(644, 333),(670, 187)],
    ("RC1C3", "RC2C5"): [(670, 187), (678, 140), (545, 123), (534, 139), (518, 179),(435, 235)],
}

# Paths
# paths = {
#     "PATH1": ["RC1C1", "RC1C2", "RC1C3", "RC2C5"],
#     "PATH2": ["RC1C1","RC2C1", "RC2C2", "RC2C3", "RC2C4", "RC2C5"]
# }

# Traffic data
trafficData = {
    "RC1C1": {
        "coordinates": (103, 393),
        "pathcoordinates": [(103, 393), (103, 393)],
        "scores": {
            "00": -1, "01": -1, "02": -1, "03": -1, "04": -1, "05": -1,
            "06": -1, "07": -1, "08": -1, "09": -1, "10": -1, "11": -1,
            "12": -1, "13": -1, "14": -1, "15": -1, "16": -1, "17": -1,
            "18": -1, "19": -1, "20": -1, "21": -1, "22": -1, "23": -1
        }
    },
    "RC1C2": {
        "coordinates": (236, 317),
        "pathcoordinates": [(237, 355), (99, 438)],
        "scores": {
            "00": -1, "01": -1, "02": -1, "03": -1, "04": -1, "05": -1,
            "06": -1, "07": -1, "08": -1, "09": -1, "10": -1, "11": -1,
            "12": -1, "13": -1, "14": -1, "15": -1, "16": -1, "17": -1,
            "18": -1, "19": -1, "20": -1, "21": -1, "22": -1, "23": -1
        }
    },
    "RC1C3": {
        "coordinates": (435, 199),
        "pathcoordinates": [(434, 235), (237, 355)],
        "scores": {
            "00": -1, "01": -1, "02": -1, "03": -1, "04": -1, "05": -1,
            "06": -1, "07": -1, "08": -1, "09": -1, "10": -1, "11": -1,
            "12": -1, "13": -1, "14": -1, "15": -1, "16": -1, "17": -1,
            "18": -1, "19": -1, "20": -1, "21": -1, "22": -1, "23": -1
        }
    },
    "RC2C1": {
        "coordinates": (199, 473),
        "pathcoordinates": [(199, 515), (99, 438)],
        "scores": {
            "00": -1, "01": -1, "02": -1, "03": -1, "04": -1, "05": -1,
            "06": -1, "07": -1, "08": -1, "09": -1, "10": -1, "11": -1,
            "12": -1, "13": -1, "14": -1, "15": -1, "16": -1, "17": -1,
            "18": -1, "19": -1, "20": -1, "21": -1, "22": -1, "23": -1
        }
    },
    "RC2C2": {
        "coordinates": (299, 482),
        "pathcoordinates": [(299, 522), (249, 535), (199, 522)],
        "scores": {
            "00": -1, "01": -1, "02": -1, "03": -1, "04": -1, "05": -1,
            "06": -1, "07": -1, "08": -1, "09": -1, "10": -1, "11": -1,
            "12": -1, "13": -1, "14": -1, "15": -1, "16": -1, "17": -1,
            "18": -1, "19": -1, "20": -1, "21": -1, "22": -1, "23": -1
        }
    },
    "RC2C3": {
        "coordinates": (420, 367),
        "pathcoordinates": [(424, 404), (318, 505)],
        "scores": {
            "00": -1, "01": -1, "02": -1, "03": -1, "04": -1, "05": -1,
            "06": -1, "07": -1, "08": -1, "09": -1, "10": -1, "11": -1,
            "12": -1, "13": -1, "14": -1, "15": -1, "16": -1, "17": -1,
            "18": -1, "19": -1, "20": -1, "21": -1, "22": -1, "23": -1
        }
    },
    "RC2C4": {
        "coordinates": (644, 293),
        "pathcoordinates": [(644, 333), (624, 333), (444, 384), (424, 404)],
        "scores": {
            "00": -1, "01": -1, "02": -1, "03": -1, "04": -1, "05": -1,
            "06": -1, "07": -1, "08": -1, "09": -1, "10": -1, "11": -1,
            "12": -1, "13": -1, "14": -1, "15": -1, "16": -1, "17": -1,
            "18": -1, "19": -1, "20": -1, "21": -1, "22": -1, "23": -1
        }
    },
    "RC2C5": {
        "coordinates": (660, 207),
        "pathcoordinates": [(670, 187), (678, 140), (545, 123), (534, 139), (518, 179), (435, 235)],
        "scores": {
            "00": -1, "01": -1, "02": -1, "03": -1, "04": -1, "05": -1,
            "06": -1, "07": -1, "08": -1, "09": -1, "10": -1, "11": -1,
            "12": -1, "13": -1, "14": -1, "15": -1, "16": -1, "17": -1,
            "18": -1, "19": -1, "20": -1, "21": -1, "22": -1, "23": -1
        }
    }
}
