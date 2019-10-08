%!assert(islogical(is_folder))
%!test ~is_folder('0984yr09uj8yfeaas918whfe98h41phfoiSDVarasAf8da1jflasjfdsdf');
%!test is_folder('.');

function ret = is_folder(path)
% overloading doesn't work in Octave since it is a core *library* function
% there doesn't appear to be a solution besides renaming this function.

if exist('isfolder', 'builtin') == 5 || exist('isfolder', 'file') == 2
  ret = isfolder(path);
else
  ret = exist(path, 'dir') == 7;
end

end % function