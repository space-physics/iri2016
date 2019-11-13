%!assert(islogical(isoctave))
%!assert(isoctave)
function isoct = isoctave()
persistent oct;

if isempty(oct)
    oct = exist('OCTAVE_VERSION', 'builtin') == 5;
end

isoct=oct; % has to be a separate line/variable for matlab

end
