import { ProductCard } from "@point_of_sale/app/components/product_card/product_card";
import { patch } from "@web/core/utils/patch";

patch(ProductCard, {
    props: {
        ...ProductCard.props,
        categoryName: { type: [String, Boolean], optional: true },
    },

    defaultProps: {
        ...ProductCard.defaultProps,
        categoryName: false,
    },
});

patch(ProductCard.prototype, {
    get resolvedCategoryName() {
        if (this.props.categoryName) {
            return this.props.categoryName;
        }

        const product = this.props.product;
        if (!product) return false;

        const cats = product.pos_category_ids;
        if (cats && cats.length) {
            const first = cats[0];
  
            if (first && typeof first === "object" && first.name) {
                return first.name;
            }
  
            if (this.env.pos) {
                const cat = this.env.pos.models["pos.category"]?.getBy("id", first);
                if (cat && cat.name) return cat.name;
            }
        }

        return false;
    },
});
