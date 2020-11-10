classdef TestUnit < matlab.unittest.TestCase

methods (Test)

function test_simple(tc)
time = datetime(2015,12,13,10,0,0);
glat = 65.1;
glon = -147.5;
altkmrange = [100,1000,10];

iono = iri2016.iri2016(time, glat, glon, altkmrange);

tc.verifyEqual(iono.Ne(11), 3.986688e9, 'RelTol', 1e-4)
end

end
end
