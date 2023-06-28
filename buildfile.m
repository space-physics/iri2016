function plan = buildfile
plan = buildplan(localfunctions);
plan.DefaultTasks = "test";
plan("test").Dependencies = "check";
end

function checkTask(~)
% Identify code issues (recursively all Matlab .m files)
issues = codeIssues("+iri2016");
assert(isempty(issues.Issues), formattedDisplayText(issues.Issues))
end

function testTask(~)
r = runtests('iri2016', strict=true, UseParallel=false);
% UseParallel can be a lot slower, especially on Mac
assert(~isempty(r), "No tests were run")
assertSuccess(r)
end
