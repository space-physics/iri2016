function iono = iri2016(time,glat,glon,altkmrange)

exe = '../bin/iri2016_driver';

t = num2str(datevec(time));


[status,dat] = system([exe, ' ', t,...
                       ' ',num2str(glat),' ',num2str(glon),...
                       ' ',num2str(altkmrange(1)),' ',num2str(altkmrange(2)),' ',num2str(altkmrange(3))]);
if status ~= 0, error(dat), end

arr = sscanf(dat, '%f', [12,Inf]);



iono.altkm = arr(1,:);
iono.Ne = arr(2,:);
iono.Tn = arr(3,:);
iono.Ti = arr(3,:);
iono.Te = arr(3,:);

end
%{
figure
semilogx(iono.Ne, iono.altkm)
figure
semilogx(iono.O2p, iono.altkm)
%}