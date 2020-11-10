classdef TestLint < matlab.unittest.TestCase

properties
TestData
end

properties (TestParameter)
file = get_files()
end

methods (TestClassSetup)

function get_files(tc)
import matlab.unittest.constraints.IsFile
import matlab.unittest.constraints.IsFolder

cwd = fileparts(mfilename('fullpath'));
cfg_file = fullfile(cwd, "MLint.txt");

tc.assumeThat(cfg_file, IsFile)

tc.TestData.cfg_file = cfg_file;

end

end


methods (Test)

function test_lint(tc, file)
res = checkcode(file, "-config=" + tc.TestData.cfg_file, "-fullpath");

for j = 1:length(res)
  tc.verifyFail(append(file, ":", int2str(res(j).line), " ", res(j).message))
end
end

end

end


function filenames = get_files()
cwd = fileparts(mfilename('fullpath'));
flist = dir(fullfile(cwd, '/**/*.m'));
for i = 1:length(flist)
 filenames{i} = fullfile(flist(i).folder, flist(i).name); %#ok<AGROW>
end
end
