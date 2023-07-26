from locations.statscollectors import expand_dict, compress_dict

expanded = {
    "atp": {
        "field": {
            "city": {
                "missing": 25,
            },
            "country": {
                "from_spider_name": 50,
                "missing": 10,
            },
        },
    },
    "finish_reason": "finished",
}

compressed = {
    "atp/field/city/missing": 25,
    "atp/field/country/from_spider_name": 50,
    "atp/field/country/missing": 10,
    "finish_reason": "finished",
}


def test_expand_dict():
    assert expanded == expand_dict(compressed)


def test_compress_dict():
    assert compressed == compress_dict(expanded)
