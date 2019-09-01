import functools
from RecordLib.crecord import CRecord
from RecordLib.common import Sentence, Charge
from RecordLib.case import Case
import re
import redis

class RedisHelper:

    def __init__(self, host, port, db, env: str, decode_responses=False):
        """ initialize the redis helper

        This helper is for storing the possible values that different elements of this Project's domain can take. For example, it will collect a redis set of all the different statutes that we see.

        The purpose is to generate a store helps developers understand what the different options could be for different fields. We can also use it to generate tests based on real data.

        This doesn't log everything. It deliberately doesn't store anything identifiable (doesn't store anything from "Person", for example).

        Args:
            r: a redis client from redis-py
            env: a string indicating the key namespace that all keys should get added to.
        """
        self.r = redis.Redis(host=host, port=port, db=db, decode_responses=decode_responses)
        self.env = env

    def sadd(self, key, obj):
        """ Default redis_sadd method

        """
        if not re.match("^" + self.env + ":", key):
            key = self.env + ":" + key
        if obj is None:
            obj = ""
        self.r.sadd(key, obj)

    def sadd_sentence(self, sentence: Sentence) -> None:
        """
        Add a sentence to the redis store
        """
        self.sadd(self.env + ":sentence:type", sentence.sentence_type)
        self.sadd(self.env + ":sentence:period", sentence.sentence_period)


    def sadd_charge(self, charge: Charge) -> None:
        for attr in ["offense", "disposition", "grade", "statute"]:
            self.sadd(self.env + ":charge:" + attr, getattr(charge, attr))
        for sentence in charge.sentences:
            self.sadd_sentence(sentence)

    def sadd_case(self, case: Case) -> None:
        """
        Store components of a Case in the redis store.
        """
        for attr in ["status", "county", "fines_and_costs", "judge"]:
            self.sadd(self.env + ":case:" + attr, getattr(case, attr))
        for charge in case.charges:
            self.sadd_charge(charge)


    def sadd_crecord(self, rec: CRecord) -> None:
        """
        Add the components of a CRecord to the redis store.
        """
        for case in rec.cases:
            self.sadd_case(case)
