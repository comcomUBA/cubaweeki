// From: https://hernan4444.github.io/iic2026/otros/barchart-race

// set the dimensions and margins of the graph
const barSize = 24
const rowCount = 17;
const margin = { top: 0, right: 0, bottom: 20, left: 160 };
const width = 800 - margin.left - margin.right;
const height = margin.top + barSize * rowCount + margin.bottom;

const formatNumber = d3.format(",d");
const scale = d3.scaleOrdinal(d3.schemeTableau10);
const color = (d) => scale(d.name);

loadDatabase = () => {
    d3.selectAll('g').interrupt();
    d3.selectAll('rect').interrupt();
    d3.selectAll('text').interrupt();
    d3.select('#dataviz').select('svg').remove()

    // append the svg object to the body of the page
    const svg = d3.select("#dataviz")
        .append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform", `translate(${margin.left}, ${margin.top})`);

    const duration = 150;
    const formatDate = d3.utcFormat("%Y-%m-%d");

    d3.json(`./edits.json?t=${Date.now()}`, d3.autoType,).then(async function (data) {
        data.sort((a, b) => d3.ascending(a.timestamp, b.timestamp));
        const names = new Set()
        const partial = new Map()
        const keyframes = []
        for (const row of data) {
            names.add(row.username);
            partial.set(row.username, (partial.get(row.username) || 0) + 1);
            const frame_data = [...partial.entries()]
                .map(v => ({ name: v[0], value: v[1] }))
                .sort((a, b) => d3.descending(a.value, b.value))
		.map((v, i) => ({ name: v.name, value: v.value, rank: i }));
            keyframes.push([new Date(row.timestamp * 1000), frame_data]);
        }

        // Guardar información sobre la instancia previa y posterior de cada dato
        const nameframes = d3.groups(keyframes.flatMap(([, data]) => data), d => d.name)
        const prev = new Map(nameframes.flatMap(([, data]) => d3.pairs(data, (a, b) => [b, a])))
        const next = new Map(nameframes.flatMap(([, data]) => d3.pairs(data)))

        x = d3.scaleLinear([0, 1], [5, width - margin.right])
        y = d3.scaleBand()
            .domain(d3.range(rowCount + 1))
            .rangeRound([margin.top, margin.top + barSize * (rowCount + 1 + 0.1)])
            .padding(0.1)
        yu = (i) => {
            return y(i) || y(rowCount)
        }

        let bar = svg.append("g")
            .attr("fill-opacity", 0.6)
            .selectAll("rect");

        const g = svg.append("g").attr("transform", `translate(0,${margin.top})`);

        const axis = d3
            .axisTop(x)
            .ticks(width / 160)
            .tickSizeOuter(0)
            .tickSizeInner(-barSize * (rowCount + y.padding()))
            .tickFormat(d => formatNumber(d).replaceAll(",", "."));

        let label = svg.append("g")
            .style("font", "bold 12px")
            .style("font-variant-numeric", "tabular-nums")
            .attr("dominant-baseline", "central")
            .selectAll("text");

        const now = svg.append("text")
            .style("font", `bold ${barSize}px`)
            .style("font-variant-numeric", "tabular-nums")
            .attr("text-anchor", "end")
            .attr("x", width - 6)
            .attr("y", height - margin.bottom/2)
            .attr("dy", "0.32em")
            .text(formatDate(keyframes[0][0]));


        for (const [date, data] of keyframes) {
            const transition = svg.transition().duration(duration).ease(d3.easeLinear);

            g.transition(transition).call(axis);
            g.select(".tick:first-of-type text").remove();
            g.selectAll(".tick:not(:first-of-type) line").attr("stroke", "rgba(0, 0, 0, 0.3)");
            g.select(".domain").remove();

            x.domain([0, d3.max(data, (d) => d.value) * 1.1])

            bar = bar.data(data.slice(0, rowCount), d => d.name)
                .join(
                    enter => enter.append("rect")
                        .attr("fill", color)
                        .attr("height", y.bandwidth())
                        .attr("x", x(0))
                        .attr("y",     d => yu((prev.get(d) || d).rank))
                        .attr("width", d =>  x((prev.get(d) || d).value) - x(0)),

                    update => update.transition(transition)
                        .attr("y",     d => y(d.rank))
                        .attr("width", d => x(d.value) - x(0)),

                    exit => exit.transition(transition).remove()
                        .attr("y",     d => y((next.get(d) || d).rank))
                        .attr("width", d => x((next.get(d) || d).value) - x(0))
                )

            label = label
                .data(data.slice(0, rowCount), d => d.name)
                .join(
                    enter => {
                        let text = enter.append("g")
                            .attr("transform", d => `translate(0,${yu((prev.get(d) || d).rank)})`)

                        text.append("text")
                            .attr("y", y.bandwidth() / 2)
                            .attr("x", 0)
                            .attr("text-anchor", "end")
                            .text(d => d.name)

                        text.append("text")
                            .attr("class", 'value')
                            .attr("transform", d => `translate(${x((prev.get(d) || d).value)}, 0)`)
                            .attr("x", 4)
                            .attr("y", y.bandwidth() / 2)
                            .attr("fill-opacity", 0.7)
                            .attr("font-weight", "normal")
                            .attr("text-anchor", "start")

                        return text;
                    },

                    update => {
                        update = update.transition(transition)
                        update.attr("transform", d => `translate(0,${y(d.rank)})`)
                        update.select(".value")
                            .attr("transform", d => `translate(${x(d.value)}, 0)`)
                            .tween("text",     d => textTween((prev.get(d) || d).value, d.value))
                        return update
                    },

                    exit => exit.transition(transition).remove()
                        .attr("transform", d => `translate(0,${y((next.get(d) || d).rank)})`)
                        .call(g => g.select("tspan")
                        .tween("text", d => textTween(d.value, (next.get(d) || d).value)))
                )
            await transition.end().then(() => now.text(formatDate(date)));
        }

        function textTween(a, b) {
            const i = d3.interpolateNumber(a, b);
            return function (t) {
                this.textContent = formatNumber(i(t)).replaceAll(",", ".");
            };
        }
    })

    const css = dataviz.childNodes[0].style
    css.fontFamily = "sans-serif"
    css.fontWeight = "bold"
    css.fontSize = "12px"
}

document.addEventListener("DOMContentLoaded", function(event) {
    loadDatabase();
});
