const chakram = require('chakram'),
    util = require('util'),
    expect = chakram.expect,
    host = process.env.HOST || "localhost",
    port = process.env.PORT || 5000;

const baseAddress = util.format('http://%s:%s/interview/api/v1.0', host, port);

describe('results/', () => {
    const url = util.format('%s/%s', baseAddress, 'results');

    it('should respond with valid types', () => {
        var response = chakram.get(url);
        expect(response).to.have.status(200);
        expect(response).to.have.schema({
            type: "array",
            area_code: {
                type: "string"
            },
            phone_number: {
                type: "string"
            },
            report_count: {
                type: "string"
            },
            comment: {
                type: "string"
            }
        });
        return chakram.wait();
    });

    it('should respond with valid data', () => {
        var response = chakram.get(url);
        expect(response).to.have.status(200);
        expect(response).to.have.json(numbers => {
            numbers.forEach(number => {
                expect(Number.parseInt(number.area_code)).to.not.be.NaN;
                expect(number.phone_number.includes(number.area_code)).to.be.true;
                expect(Number.parseInt(number.report_count)).to.not.be.NaN;
            });
        });
        return chakram.wait();
    });

    it('should have 2 entries with when count = 2', () => {
        var response = chakram.get(url + '?count=2');
        expect(response).to.have.status(200);
        expect(response).to.have.json(numbers => {
            expect(numbers.length).to.equal(2);
        });
        return chakram.wait();
    });

    it('should have status 400 with invalid count', () => {
        var response = chakram.get(url + '?count=abcd');
        expect(response).to.have.status(400);
        return chakram.wait();
    });

    it('should respond with 404 when no results are found with area code', () => {
        var response = chakram.get(url + '?area_code=555');
        expect(response).to.have.status(404);
        return chakram.wait();
    });

    it('should respond with 200 when an area code exist', () => {
        var response = chakram.get(url + '?area_code=770');
        expect(response).to.have.status(200);
        expect(response).to.have.json(numbers => {
            expect(numbers.length).to.be.above(0);
        });
        return chakram.wait();
    });

    it('should respond with 200 with valid area code and valid count', () => {
        var response = chakram.get(url + '?area_code=770&count=1');
        expect(response).to.have.status(200);
        expect(response).to.have.json(numbers => {
            expect(numbers.length).to.be.above(0);
        });
        return chakram.wait();
    });

    it('should have status 400 with invalid count but valid area code', () => {
        var response = chakram.get(url + '?count=abcd&area_code=770');
        expect(response).to.have.status(400);
        return chakram.wait();
    });

    it('should have status 404 with valid count but invalid area code', () => {
        var response = chakram.get(url + '?count=1&area_code=abc');
        expect(response).to.have.status(404);
        return chakram.wait();
    });
});