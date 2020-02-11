url=https://www.emnlp-ijcnlp2019.org/program/accepted/
root=section.page__content#page_body.page

[e:h2:root]
[p:+ ul li: e] ->
[
	{
		id: "id",
		t_: [0:span:p] -> elem.text.strip() + '.',
		title: t_,
		hash: md5_hex(t_),
		authors: [0:i:p] ->
				 [elem.text.replace(' and ',',').split(',')] ->
				 [
					a_= elem.strip(),
					len(a_) > 0 ? a_
				 ],
		type: e.text
	}
]
