%!assert(islogical(is_file))
%!test ~is_file('0984yr09uj8yfeaas918whfe98h41phfoiSDVarasAf8da1jflasjfdsdf');
%!test is_file('.');

function ret = is_file(path)
% overloading doesn't work in Octave since it is a core *library* function
% there doesn't appear to be a solution besides renaming this function.

if exist('isfile', 'builtin') == 5 || exist('isfile', 'file') == 2
  ret = isfile(path);
else
  ret = exist(path, 'file') == 2;
end

end % function