function exe = pyexe()
%% find Python 3 executable for Matlab and GNU Octave

%% Matlab >= R2019b
try %#ok<*TRYNC>
  env = pyenv();
  exe = char(env.Executable);
  return
end
%% Matlab <= R2019a
try
  [~, exe] = pyversion();
  if ~isempty(exe), return, end
end
%% plain Python
version_test_str = ['python -c "import sys; print(sys.version_info >= (3, 6), end=', "''", ')"'];
exe_loc_str = ['python -c "import sys; print(sys.executable, end=', "''", ')"'];

[status, ret] = system(version_test_str);
if status==0 && strcmp(ret, 'True')
  [~, exe] = system(exe_loc_str);
  return
end
%% Anaconda Python
try
  [status, ret] = system(['conda activate && ', version_test_str]);
  if status==0 && strcmp(ret, 'True')
    [~, exe] = system(['conda activate && ', exe_loc_str]);
    return
  end
end

error(['could not find Python executable: ', exe])

end % function