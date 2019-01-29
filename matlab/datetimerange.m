function times = datetimerange(t0, t1, ts)

validateattributes(ts, {'numeric'}, {'scalar', 'positive'})
% ts: seconds

if ~isscalar(t0), t0 = datenum(t0); end
if ~isscalar(t1), t1 = datenum(t1); end

times = t0:ts/86400:t1;

end
