function setup_meson(srcdir, builddir)
%% setup using Meson+Fortran compiler

validateattributes(srcdir,{'char'},{'vector'})
validateattributes(builddir,{'char'},{'vector'})


[status, ret] = system(['meson setup ',builddir,' ',srcdir]);
if status~=0, error(ret), end
disp(ret)

[status, ret] = system(['ninja -C ',builddir]);
if status~=0, error(ret), end
disp(ret)

disp('Fortran compilation complete')
end
