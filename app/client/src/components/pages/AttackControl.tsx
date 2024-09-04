// import React, { useEffect } from "react";
// import { getSavedAttacks } from "../../middleware/api/functions/getSavedAttacks";
// import { useClientStore } from "../../stores/client-store";
// import {
//   Card,
//   CardHeader,
//   CardTitle,
//   CardContent,
//   CardDescription,
// } from "./Card";
// import {
//   Card,
//   CardHeader,
//   CardTitle,
//   CardContent,
//   CardDescription,
// } from "../ui/card";
import { useServicesStore } from "@/stores/services-store";
import { useEffect } from "react";

const AttackControl = () => {
  useEffect(() => {
    // getSavedAttacks();
  }, []);
  const { feeders, neuralNetworks, offlineFeeders, defaults } =
    useServicesStore();

  console.log(feeders, neuralNetworks, offlineFeeders, defaults);

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">Attack Control</h1>
      <div>
        <h2 className="text-xl font-semibold mb-2">Saved Attacks</h2>
        <ul className="space-y-4"></ul>
      </div>
    </div>
  );
};

export default AttackControl;
