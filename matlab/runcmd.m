function runcmd(cmd)
narginchk(1,1)
validateattributes(cmd,{'char'},{'vector'})

[status, ret] = system(cmd);
if status~=0, error(ret), end
disp(ret)
end
