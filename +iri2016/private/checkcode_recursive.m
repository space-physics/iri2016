function [fail, N] = checkcode_recursive(folder, tc, cfg_file)
%% lints each Matlab .m file in folder.
% distinct from mlintrpt() in that this function is all CLI instead of GUI
%
% Copyright (c) 2020 Michael Hirsch (MIT License)
arguments
  folder (1,1) string
  tc matlab.unittest.TestCase
  cfg_file string = string.empty
end

import matlab.unittest.Verbosity

if ~isempty(cfg_file)
  assert(isfile(cfg_file), "lint config file does not exist " + cfg_file)
  cfg = "-config=" + cfg_file;
else
  cfg = "-struct";
end

assert(isfolder(folder), folder + " is not a folder")

flist = dir(folder + "/**/*.m");
N = length(flist);

assert(N > 0, "no files found to lint in " + folder)

fail = false;

for i = 1:N
  file = fullfile(flist(i).folder, flist(i).name);

  res = checkcode(file, cfg);
  if isempty(res)
    continue
  end

  fail = true;
  for j = 1:length(res)
    tc.log(Verbosity.Terse, append(file, ":", int2str(res(j).line), " ", res(j).message))
  end
end % for

end % function
