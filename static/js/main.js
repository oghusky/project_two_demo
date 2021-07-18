
  d3
  .json('/api/sql_data')
  .then(data=>{
    console.log(data);

    const plot = {
      "$schema": "https://vega.github.io/schema/vega-lite/v4.json",
      "description": "A scatterplot showing horsepower and miles per gallons for various cars.",
      "data": { values: data.splice(0,20) },
      "mark": "point",
      "encoding": {
        "x": { "field": "Name", "type": "nominal" },
        "y": { "field": "Attack", "type": "quantitative" }
      }
    }
    vegaEmbed("#plot", plot)
  })
  .catch(err => console.log(err));