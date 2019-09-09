function runcmd(cmd)

validateattributes(cmd,{'char'},{'vector'})

[status, ret] = system(cmd);
if status~=0, error(ret), end
disp(ret)
end
