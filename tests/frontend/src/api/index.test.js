import * as api from "frontend/src/api"


describe('removing null values from objects', () => {
    it('removes keys with null values from an object', () => {
        const myObj = {
            something: "hello",
            nothing: null,
        }
        const result = api.removeNullValues(myObj);
        expect(result).toEqual({
            something: "hello"
        })
    })
})