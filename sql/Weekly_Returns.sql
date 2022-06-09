select
    trunc(date_trunc('Week',most_recent_item_fulfilled)) as fulfillment_date_start
    , style_name
    , sum(qty_fulfill) as fulfillments
    , nullif(sum(case when return_created_date is not null then 1 else 0 end),0) as returns
    , returns * 1.0 / fulfillments as rate
from product_pull.levity_fulfillments
where fulfillment_date_start is not null
group by 1,2
order by 1 desc, 2;