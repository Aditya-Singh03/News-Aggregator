import {
  Carousel,
  CarouselContent,
  CarouselItem,
  CarouselNext,
  CarouselPrevious,
} from "@/components/ui/carousel";

import { Card, CardContent } from "@/components/ui/card";
import { useEffect, useState } from "react";
import { BACKEND_URL } from "@/utils/constants";
import { SourceInfo } from "@/types";
import { dateFormatter, linkFormatter, nameFormatter } from "@/utils/formatter";

function SourceCarousel(SourceCarouselProps: { sourceIds: Array<string> }) {
  const sourceIds = SourceCarouselProps.sourceIds;

  const SourceContainer = (orgSrc: SourceInfo) => {
    const [source, setSource] = useState(orgSrc);
    useEffect(() => {
      fetch(
        `${BACKEND_URL}/aggregator/get-aggregation?source_id=${orgSrc.id}`,
        {
          method: "GET",
        }
      )
        .then((res) => res.json())
        .then((json) => json.source)
        .then((source): void => {
          setSource(source);
        });
    }, []);

    return (
      <CarouselItem className="h-full md:basis-1/1 lg:basis-1/2">
        <div className="p-1">
          <Card className="bg-inherit text-white h-[250px]">
            <CardContent className="p-6 overflow-hidden">
              <h2>{source.title}</h2>
              <span className="flex gap-2 mt-3 mb-3">
                <p>{source.author && nameFormatter(source.author)}</p>
                <p>{source.date && dateFormatter(source.date)}</p>
              </span>
              <a className="text-blue-500 underline" href={source.link}>
                {source.link && linkFormatter(source.link)}
              </a>
            </CardContent>
          </Card>
        </div>
      </CarouselItem>
    );
  };

  const sources = Array.from(Array(sourceIds.length), (_, i) =>
    SourceContainer({
      id: sourceIds[i],
      author: "",
      date: "",
      title: "",
      link: "",
    })
  );

  return (
    <Carousel
      opts={{
        align: "center",
      }}
      className="w-full max-w-3xl h-full"
      >
      <CarouselPrevious variant={"default"} className="" />
      <CarouselNext variant={"default"} className="" />
      <CarouselContent className="gap-1">{sources}</CarouselContent>
    </Carousel>
  );
}

export default SourceCarousel;
