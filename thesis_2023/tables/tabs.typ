= Safiya's tables
#figure(
    table(
        columns: (auto, auto, auto),
        inset: 15pt,
        stroke: 3pt,
        // Column headers
        [#align(center + horizon)[#text(size: 16pt)[*Political party*]]],
        [#text(size: 14pt)[
            *Future immigration should*\
            #line(length: 100%)
            #grid(
                columns: (1fr, 1fr),
                align(left)[*Stay the same or increase*],
                align(right)[*Decrease*]
            )
        ]],
        [#align(center + bottom)[#text(size: 14pt)[*Total*]]],
        // Labels cell
        [
            #table(
                columns: (1fr),
                inset: 15pt,
                stroke: none,
                [
                    #grid(
                        columns: (1fr, 1fr),
                        align(left)[*Democrat*],
                        align(right)[
                            est.\
                            #text(size: 0.8em)[s.e.]
                        ]
                    )
                ],
                [
                    #grid(
                        columns: (1fr, 1fr),
                        align(left)[*Independent*],
                        align(right)[
                            est.\
                            #text(size: 0.8em)[s.e.]
                        ]
                    )
                ],
                [
                    #grid(
                        columns: (1fr, 1fr),
                        align(left)[*Republicans*],
                        align(right)[
                            est.\
                            #text(size: 0.8em)[s.e.]
                        ]
                    )
                ]
            )
    ],
    // Data cell
    [
        #table(
            columns: (1fr),
            inset: 15pt,
            stroke: none,
            [
                #grid(
                    columns: (1fr, 1fr),
                    align(left)[
                        66.8%\
                        #text(size: 0.8em)[1.4%]
                    ],
                    align(right)[
                        33.2%\
                        #text(size: 0.8em)[1.42%]
                    ]
                )
            ],
            [
                #grid(
                    columns: (1fr, 1fr),
                    align(left)[
                        66.6%\
                        #text(size: 0.8em)[.4%]
                    ],
                    align(right)[
                        33.4%\
                        #text(size: 0.8em)[.29%]
                    ]
                )
            ],
            [
                #grid(
                    columns: (1fr, 1fr),
                    align(left)[
                        43%\
                        #text(size: 0.8em)[1.1%]
                    ],
                    align(right)[
                        57%\
                        #text(size: 0.8em)[1.5%]
                    ]
                )
            ]
        )
    ],
    // Totals cell
    [
        #table(
            columns: (1fr),
            // NOTE: Inset is different from the above for alignment purposes
            inset: 20pt,
            stroke: none,
            [100%],
            [100%],
            [100%]
        )
    ]
    )
)
