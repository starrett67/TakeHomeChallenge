const chakram = require('chakram'),
    util = require('util'),
    expect = chakram.expect,
    host = process.env.HOST || "localhost",
    port = process.env.PORT || 5000;

const baseAddress = util.format('http://%s:%s/interview/api/v1.0', host, port);

describe('resultsForArea/', () => {
    const url = util.format('%s/%s', baseAddress, 'resultsForArea');

    it('should respond with valid types', () => {
        var response = chakram.get(url + '/770');
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
        var response = chakram.get(url + '/770');
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

    it('should respond with 404 when no results are found', () => {
        var response = chakram.get(url + '/555');
        expect(response).to.have.status(404);
        return chakram.wait();
    })    
});