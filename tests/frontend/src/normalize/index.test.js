import { normalizeCRecord, denormalizeSourceRecords } from "frontend/src/normalize";
import { initialCrecordState } from "frontend/src/reducers/crecord"

describe('crecord normalizers', () => {
    it('should turn an empty crecord nested object into empty normalized components.', () => {
        const crecord = initialCrecordState;
        const normalized = normalizeCRecord(crecord)
        expect(normalized).toEqual({
            entities: {
                cRecord: {
                    root: {
                        cRecord: {
                            root: {
                                cases: [],
                            }
                        },
                        cases: [],
                        charges: {},
                        id: "root",
                        sentences: {}
                    }
                }
            },
            result: "root"
        })
    })
})


describe('normalizing sourceRecords', () => {
    it('should denormalize from the normalized shape', () => {
        const normalized = {
            allIds: ["abc", "123"],
            allSourceRecords: {
                "abc": {
                    id: "abc",
                    caption: "A v. B",
                    court: "CP", 
                },
                "123": {
                    id: "123",
                    caption: "1 v 2",
                    court: "MD",
                },
            }
        }

        const denormalized = denormalizeSourceRecords(normalized)
        expect(denormalized).toEqual(
            [
                {
                    id: "abc",
                    caption: "A v. B",
                    court: "CP", 
                },
                {
                    id: "123",
                    caption: "1 v 2",
                    court: "MD",
                }
            ]
        )
    })
})