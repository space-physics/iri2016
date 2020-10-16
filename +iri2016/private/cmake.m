function cmake(src_dir)
% build program using CMake and default generator
% to specify generator with CMake >= 3.15 set environment variable CMAKE_GENERATOR
arguments
  src_dir (1,1) string
end

fix_macos()

cmd = "cmake --version";
ret = system(cmd);
if ret ~= 0
  error('cmake:runtime_error', 'CMake not found')
end

cmd = "ctest -S " + fullfile(src_dir, "setup.cmake") +  " -VV";


if ~isfolder(src_dir)
  error("cmake:file_not_found", "source directory not found: " + src_dir)
end

ret = system(cmd);
if ret ~= 0
  error('cmake:runtime_error', 'error building with CMake')
end

end


function fix_macos()

%% MacOS PATH workaround
% Matlab does not seem to load .zshrc or otherwise pickup shell "export" like
% Matlab on Linux or Windows does, so we apply these MacOS-specific workaround
if ~ismac
  return
end

sys_path = getenv("PATH");
needed_paths = "/usr/local/bin";
for np = needed_paths
  if isfolder(np) && ~contains(sys_path, np)
    sys_path = np + pathsep + sys_path;
  end
end

setenv('PATH', sys_path)

end % function
