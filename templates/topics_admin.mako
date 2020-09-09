<%inherit file="base.mako"/>

% for topic in data["topics"]:
	${topic["id"]} ${topic["topic"]["cze"]} ${topic["topic"]["eng"]} ${topic["description"]["cze"]} ${topic["description"]["eng"]}
% endfor