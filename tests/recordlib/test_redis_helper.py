"""
redis_sadd is for saving different bits of info to redis sets, so we develop a collection of the possible values that different items might have. We can see what values "statute" might take, for example.

"""
import pytest


def test_redis_sadd(redis_helper):
    r = redis_helper.r
    r.delete("testset")
    r.sadd("testset", "val1")
    r.sadd("testset", "val2")
    assert r.smembers("testset") == {"val1", "val2"}
    r.delete("testset")


def test_sadd_crecord(redis_helper, example_crecord):

    redis_helper.sadd_crecord(example_crecord)
    assert redis_helper.r.smembers("test:charge:disposition") == {charge.disposition  for case in example_crecord.cases for charge in case.charges}

    assert redis_helper.r.smembers("test:charge:offense") == {charge.offense  for case in example_crecord.cases for charge in case.charges}

    assert redis_helper.r.smembers("test:charge:grade") == {charge.grade  for case in example_crecord.cases for charge in case.charges}

    assert redis_helper.r.smembers("test:charge:statute") == {charge.statute  for case in example_crecord.cases for charge in case.charges}
