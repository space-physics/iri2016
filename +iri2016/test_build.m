function tests = test_build
tests = functiontests(localfunctions);
end


function test_ctest(tc)
cwd = fileparts(mfilename('fullpath'));
srcdir = fullfile(cwd, "/../src/iri2016");
iri2016.cmake(srcdir)
name = "iri2016_driver";
if ispc
  name = name + ".exe";
end
tc.fatalAssertTrue(isfile(fullfile(srcdir, name)))
end