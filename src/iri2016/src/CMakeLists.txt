add_library(iri2016 OBJECT irisub.for irifun.for iritec.for iridreg.for igrf.for cira.for iriflip.for)
target_compile_options(iri2016 PRIVATE $<$<BOOL:${nowarn}>:-w>)
